from __future__ import annotations

import argparse
import bisect
import math
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path

import torch
import torch.nn.functional as F
from torch import Tensor, nn
from torch.utils.data import DataLoader, Dataset, random_split
from tqdm import tqdm



def _make_group_norm(num_channels: int) -> nn.GroupNorm:
    for num_groups in (8, 4, 2, 1):
        if num_channels % num_groups == 0:
            return nn.GroupNorm(num_groups=num_groups, num_channels=num_channels)
    raise ValueError(f"Could not build GroupNorm for {num_channels} channels.")


def _sinusoidal_position_embedding(length: int, dim: int, device: torch.device, dtype: torch.dtype) -> Tensor:
    positions = torch.arange(length, device=device, dtype=dtype).unsqueeze(1)
    frequency = torch.exp(
        torch.arange(0, dim, 2, device=device, dtype=dtype) * (-math.log(10000.0) / max(dim, 1))
    )
    angles = positions * frequency.unsqueeze(0)

    embedding = torch.zeros(length, dim, device=device, dtype=dtype)
    embedding[:, 0::2] = torch.sin(angles)
    if dim > 1:
        embedding[:, 1::2] = torch.cos(angles[:, : embedding[:, 1::2].shape[1]])
    return embedding


class ConvNormAct(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, kernel_size: int, stride: int = 1, padding: int = 0):
        super().__init__()
        self.block = nn.Sequential(
            nn.Conv2d(
                in_channels=in_channels,
                out_channels=out_channels,
                kernel_size=kernel_size,
                stride=stride,
                padding=padding,
                bias=False,
            ),
            _make_group_norm(out_channels),
            nn.GELU(),
        )

    def forward(self, x: Tensor) -> Tensor:
        return self.block(x)


class DoubleConv(nn.Module):
    def __init__(self, in_channels: int, out_channels: int):
        super().__init__()
        self.block = nn.Sequential(
            ConvNormAct(in_channels, out_channels, kernel_size=3, padding=1),
            ConvNormAct(out_channels, out_channels, kernel_size=3, padding=1),
        )

    def forward(self, x: Tensor) -> Tensor:
        return self.block(x)


class DepthTokenEncoder(nn.Module):
    def __init__(
        self,
        depth_channels: int,
        embed_dim: int,
        token_grid_size: tuple[int, int],
        context_channels: int,
    ):
        super().__init__()
        self.token_grid_size = token_grid_size

        self.encoder = nn.Sequential(
            ConvNormAct(depth_channels, 32, kernel_size=5, stride=2, padding=2),
            ConvNormAct(32, 64, kernel_size=3, stride=2, padding=1),
            ConvNormAct(64, 96, kernel_size=3, stride=2, padding=1),
            ConvNormAct(96, embed_dim, kernel_size=3, padding=1),
        )
        self.token_pool = nn.AdaptiveAvgPool2d(token_grid_size)
        self.token_projection = nn.Conv2d(embed_dim, embed_dim, kernel_size=1)
        self.context_projection = nn.Sequential(
            nn.Conv2d(embed_dim, context_channels, kernel_size=1),
            nn.GELU(),
        )
        self.token_norm = nn.LayerNorm(embed_dim)

    def forward(self, depth_sequence: Tensor) -> tuple[Tensor, Tensor]:
        batch_size, depth_steps, channels, _, _ = depth_sequence.shape
        token_grid_h, token_grid_w = self.token_grid_size

        encoded = self.encoder(depth_sequence.reshape(batch_size * depth_steps, channels, *depth_sequence.shape[-2:]))
        token_maps = self.token_projection(self.token_pool(encoded))
        token_maps = token_maps.reshape(batch_size, depth_steps, -1, token_grid_h, token_grid_w)

        depth_tokens = token_maps.permute(0, 1, 3, 4, 2).reshape(batch_size, depth_steps, token_grid_h * token_grid_w, -1)
        time_pos = _sinusoidal_position_embedding(depth_steps, depth_tokens.shape[-1], depth_tokens.device, depth_tokens.dtype)
        spatial_pos = _sinusoidal_position_embedding(
            token_grid_h * token_grid_w, depth_tokens.shape[-1], depth_tokens.device, depth_tokens.dtype
        )
        depth_tokens = depth_tokens + time_pos.view(1, depth_steps, 1, -1) + spatial_pos.view(1, 1, token_grid_h * token_grid_w, -1)
        depth_tokens = self.token_norm(depth_tokens).reshape(batch_size, depth_steps * token_grid_h * token_grid_w, -1)

        depth_context = self.context_projection(token_maps.mean(dim=1))
        return depth_tokens, depth_context


class ProprioceptiveHistoryEncoder(nn.Module):
    def __init__(self, proprio_dim: int, embed_dim: int, hidden_dim: int):
        super().__init__()
        self.input_norm = nn.LayerNorm(proprio_dim)
        self.encoder = nn.Sequential(
            nn.Linear(proprio_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, embed_dim),
        )
        self.output_norm = nn.LayerNorm(embed_dim)

    def forward(self, proprio_history: Tensor) -> Tensor:
        batch_size, history_steps, _ = proprio_history.shape
        tokens = self.encoder(self.input_norm(proprio_history))
        position_embedding = _sinusoidal_position_embedding(history_steps, tokens.shape[-1], tokens.device, tokens.dtype)
        tokens = self.output_norm(tokens + position_embedding.view(1, history_steps, -1))
        return tokens.reshape(batch_size, history_steps, -1)


class FeedForwardBlock(nn.Module):
    def __init__(self, embed_dim: int, dropout: float):
        super().__init__()
        self.block = nn.Sequential(
            nn.Linear(embed_dim, embed_dim * 4),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(embed_dim * 4, embed_dim),
            nn.Dropout(dropout),
        )

    def forward(self, x: Tensor) -> Tensor:
        return self.block(x)


class CrossAttentionBlock(nn.Module):
    def __init__(self, embed_dim: int, num_heads: int, dropout: float):
        super().__init__()
        self.query_norm = nn.LayerNorm(embed_dim)
        self.context_norm = nn.LayerNorm(embed_dim)
        self.attention = nn.MultiheadAttention(
            embed_dim=embed_dim,
            num_heads=num_heads,
            dropout=dropout,
            batch_first=True,
        )
        self.feedforward_norm = nn.LayerNorm(embed_dim)
        self.feedforward = FeedForwardBlock(embed_dim=embed_dim, dropout=dropout)

    def forward(self, query_tokens: Tensor, context_tokens: Tensor) -> Tensor:
        normalized_query = self.query_norm(query_tokens)
        normalized_context = self.context_norm(context_tokens)
        attention_output, _ = self.attention(
            query=normalized_query,
            key=normalized_context,
            value=normalized_context,
            need_weights=False,
        )
        fused = query_tokens + attention_output
        fused = fused + self.feedforward(self.feedforward_norm(fused))
        return fused


class ConditionalUNetRefiner(nn.Module):
    def __init__(self, input_channels: int, base_channels: int):
        super().__init__()
        self.enc1 = DoubleConv(input_channels, base_channels)
        self.enc2 = DoubleConv(base_channels, base_channels * 2)
        self.bottleneck = DoubleConv(base_channels * 2, base_channels * 4)
        self.dec1 = DoubleConv(base_channels * 4 + base_channels * 2, base_channels * 2)
        self.dec2 = DoubleConv(base_channels * 2 + base_channels, base_channels)
        self.output_projection = nn.Conv2d(base_channels, 1, kernel_size=1)

    def forward(self, x: Tensor) -> Tensor:
        skip_1 = self.enc1(x)
        skip_2 = self.enc2(F.max_pool2d(skip_1, kernel_size=2))
        bottleneck = self.bottleneck(F.max_pool2d(skip_2, kernel_size=2))

        x = F.interpolate(bottleneck, size=skip_2.shape[-2:], mode="bilinear", align_corners=False)
        x = self.dec1(torch.cat((x, skip_2), dim=1))
        x = F.interpolate(x, size=skip_1.shape[-2:], mode="bilinear", align_corners=False)
        x = self.dec2(torch.cat((x, skip_1), dim=1))
        return self.output_projection(x)


@dataclass
class TerrainReconstructionOutput:
    rough_heightmap: Tensor
    refined_heightmap: Tensor
    hidden_state: Tensor | None


class MultiModalTerrainReconstructor(nn.Module):
    """Cross-attention terrain reconstructor based on the paper's two-stage design.

    Expected inputs:
    - depth_data: `(B, T_depth, C, H, W)` or `(B, C, H, W)`
    - robot_info: `(B, T_prop, F)` or `(B, F)`

    The model assumes the depth images are already valid and preprocessed. It does
    not implement the paper's synthetic-depth corruption pipeline.
    """

    def __init__(
        self,
        proprio_dim: int,
        depth_channels: int = 1,
        heightmap_size: tuple[int, int] = (20, 20),
        embed_dim: int = 128,
        proprio_hidden_dim: int = 256,
        num_attention_heads: int = 4,
        num_cross_attention_layers: int = 2,
        recurrent_hidden_dim: int = 192,
        recurrent_layers: int = 1,
        token_grid_size: tuple[int, int] = (6, 8),
        refinement_context_channels: int = 32,
        refinement_base_channels: int = 32,
        dropout: float = 0.1,
    ):
        super().__init__()
        self.heightmap_size = heightmap_size

        self.depth_encoder = DepthTokenEncoder(
            depth_channels=depth_channels,
            embed_dim=embed_dim,
            token_grid_size=token_grid_size,
            context_channels=refinement_context_channels,
        )
        self.proprio_encoder = ProprioceptiveHistoryEncoder(
            proprio_dim=proprio_dim,
            embed_dim=embed_dim,
            hidden_dim=proprio_hidden_dim,
        )
        self.cross_attention_blocks = nn.ModuleList(
            [
                CrossAttentionBlock(embed_dim=embed_dim, num_heads=num_attention_heads, dropout=dropout)
                for _ in range(num_cross_attention_layers)
            ]
        )
        self.memory = nn.GRU(
            input_size=embed_dim,
            hidden_size=recurrent_hidden_dim,
            num_layers=recurrent_layers,
            batch_first=True,
            dropout=dropout if recurrent_layers > 1 else 0.0,
        )
        self.rough_decoder = nn.Sequential(
            nn.LayerNorm(recurrent_hidden_dim),
            nn.Linear(recurrent_hidden_dim, recurrent_hidden_dim * 2),
            nn.GELU(),
            nn.Linear(recurrent_hidden_dim * 2, heightmap_size[0] * heightmap_size[1]),
        )
        self.refinement_context_projection = nn.Sequential(
            nn.Conv2d(refinement_context_channels, refinement_base_channels, kernel_size=3, padding=1),
            nn.GELU(),
        )
        self.refiner = ConditionalUNetRefiner(
            input_channels=1 + refinement_base_channels,
            base_channels=refinement_base_channels,
        )

    def _prepare_depth_sequence(self, depth_data: Tensor) -> Tensor:
        if depth_data.dim() == 4:
            return depth_data.unsqueeze(1)
        if depth_data.dim() == 5:
            return depth_data
        raise ValueError(
            "depth_data must have shape (B, C, H, W) or (B, T_depth, C, H, W), "
            f"but got {tuple(depth_data.shape)}"
        )

    def _prepare_proprio_history(self, robot_info: Tensor) -> Tensor:
        if robot_info.dim() == 2:
            return robot_info.unsqueeze(1)
        if robot_info.dim() == 3:
            return robot_info
        raise ValueError(
            "robot_info must have shape (B, F) or (B, T_prop, F), "
            f"but got {tuple(robot_info.shape)}"
        )

    def forward(
        self,
        depth_data: Tensor,
        robot_info: Tensor,
        hidden_state: Tensor | None = None,
    ) -> TerrainReconstructionOutput:
        depth_sequence = self._prepare_depth_sequence(depth_data)
        proprio_history = self._prepare_proprio_history(robot_info)

        depth_tokens, depth_context = self.depth_encoder(depth_sequence)
        proprio_tokens = self.proprio_encoder(proprio_history)

        fused_tokens = proprio_tokens
        for block in self.cross_attention_blocks:
            fused_tokens = block(fused_tokens, depth_tokens)

        memory_tokens, hidden_state = self.memory(fused_tokens, hidden_state)
        rough_heightmap = self.rough_decoder(memory_tokens[:, -1]).view(-1, 1, *self.heightmap_size)

        depth_context = self.refinement_context_projection(depth_context)
        depth_context = F.interpolate(depth_context, size=self.heightmap_size, mode="bilinear", align_corners=False)

        refinement_input = torch.cat((rough_heightmap, depth_context), dim=1)
        refinement_residual = self.refiner(refinement_input)
        refined_heightmap = rough_heightmap + refinement_residual

        return TerrainReconstructionOutput(
            rough_heightmap=rough_heightmap,
            refined_heightmap=refined_heightmap,
            hidden_state=hidden_state,
        )


def compute_reconstruction_losses(
    prediction: TerrainReconstructionOutput, target_heightmap: Tensor, rough_loss_type: str = "mse"
) -> dict[str, Tensor]:
    # With small-valued targets, MSE on the rough stage yields gradients far weaker than the L1 on the
    # refined stage, so the rough decoder barely trains; "l1" gives both stages comparable gradients.
    if rough_loss_type == "l1":
        rough_loss = F.l1_loss(prediction.rough_heightmap, target_heightmap)
    elif rough_loss_type == "mse":
        rough_loss = F.mse_loss(prediction.rough_heightmap, target_heightmap)
    else:
        raise ValueError(f"Unknown rough_loss_type: {rough_loss_type}")
    refined_loss = F.l1_loss(prediction.refined_heightmap, target_heightmap)
    total_loss = rough_loss + refined_loss
    return {
        "loss": total_loss,
        "rough_loss": rough_loss,
        "refined_loss": refined_loss,
    }


class FakeTerrainReconstructionDataset(Dataset):
    def __init__(
        self,
        num_samples: int = 128,
        depth_history: int = 5,
        proprio_history: int = 50,
        proprio_dim: int = 48,
        depth_image_size: tuple[int, int] = (64, 80),
        heightmap_size: tuple[int, int] = (20, 20),
        seed: int = 0,
    ):
        super().__init__()
        generator = torch.Generator().manual_seed(seed)

        self.depth_data = torch.rand(num_samples, depth_history, 1, *depth_image_size, generator=generator) * 2.0 - 1.0
        self.robot_info = torch.randn(num_samples, proprio_history, proprio_dim, generator=generator)
        self.heightmaps = self._build_targets(heightmap_size=heightmap_size)

    def _build_targets(self, heightmap_size: tuple[int, int]) -> Tensor:
        batch_size = self.depth_data.shape[0]
        height, width = heightmap_size

        x_grid = torch.linspace(-1.0, 1.0, width).view(1, 1, 1, width)
        y_grid = torch.linspace(-1.0, 1.0, height).view(1, 1, height, 1)

        depth_summary = F.interpolate(
            self.depth_data.mean(dim=1),
            size=heightmap_size,
            mode="bilinear",
            align_corners=False,
        )
        last_robot_state = self.robot_info[:, -1]
        mean_robot_state = self.robot_info.mean(dim=1)

        pitch_like = last_robot_state[:, 0].view(batch_size, 1, 1, 1)
        roll_like = last_robot_state[:, 1].view(batch_size, 1, 1, 1)
        velocity_like = mean_robot_state[:, 2].view(batch_size, 1, 1, 1)
        gait_like = last_robot_state[:, 3].view(batch_size, 1, 1, 1)

        target = (
            0.65 * depth_summary
            + 0.15 * pitch_like * x_grid
            + 0.15 * roll_like * y_grid
            + 0.05 * velocity_like * torch.sin(math.pi * (x_grid + gait_like))
            + 0.05 * torch.cos(math.pi * (y_grid - gait_like))
        )
        return target.clamp(-2.0, 2.0)

    def __len__(self) -> int:
        return self.depth_data.shape[0]

    def __getitem__(self, index: int) -> tuple[Tensor, Tensor, Tensor]:
        return self.depth_data[index], self.robot_info[index], self.heightmaps[index]


class _ConcatenatedRows:
    """Rows of same-shaped tensors concatenated along dim 0 without copying them (they stay memory-mapped)."""

    def __init__(self, tensors: list[Tensor]):
        self.tensors = tensors
        self.offsets = [0]
        for tensor in tensors:
            self.offsets.append(self.offsets[-1] + tensor.shape[0])
        self.shape = torch.Size((self.offsets[-1], *tensors[0].shape[1:]))

    def __getitem__(self, index: int) -> Tensor:
        shard = bisect.bisect_right(self.offsets, index) - 1
        return self.tensors[shard][index - self.offsets[shard]]


class SavedTerrainReconstructionDataset(Dataset):
    """One or more collected dataset files, read lazily.

    The files are memory-mapped: depth and robot info stay on disk (cached by the OS) and each sample is read and
    converted to float32 when accessed, so datasets larger than RAM work. Only the small targets are kept in RAM.
    """

    def __init__(self, dataset_path: str | Sequence[str], target_key: str = "heightmaps"):
        super().__init__()
        dataset_paths = [dataset_path] if isinstance(dataset_path, (str, Path)) else list(dataset_path)
        shards = [torch.load(str(path), map_location="cpu", mmap=True) for path in dataset_paths]

        required_keys = {"depth_data", "robot_info", target_key}
        for path, shard in zip(dataset_paths, shards):
            missing_keys = required_keys.difference(shard)
            if missing_keys:
                missing = ", ".join(sorted(missing_keys))
                raise KeyError(f"Dataset at {path} is missing required keys: {missing}")

        self.depth_data = _ConcatenatedRows([shard["depth_data"] for shard in shards])
        self.robot_info = _ConcatenatedRows([shard["robot_info"] for shard in shards])
        self.heightmaps = torch.cat([shard[target_key].float() for shard in shards])
        self.metadata = shards[0].get("metadata", {})

        dataset_size = self.depth_data.shape[0]
        if self.robot_info.shape[0] != dataset_size or self.heightmaps.shape[0] != dataset_size:
            raise ValueError("depth_data, robot_info, and heightmaps must all contain the same number of samples.")

    def __len__(self) -> int:
        return self.depth_data.shape[0]

    def __getitem__(self, index: int) -> tuple[Tensor, Tensor, Tensor]:
        return self.depth_data[index].float(), self.robot_info[index].float(), self.heightmaps[index]


def _run_epoch(
    model: nn.Module,
    data_loader: DataLoader,
    device: torch.device,
    optimizer: torch.optim.Optimizer | None,
    target_mean: float = 0.0,
    target_std: float = 1.0,
    rough_loss_type: str = "mse",
) -> dict[str, float]:
    """Run one epoch. Losses are computed on normalized targets ``(target - target_mean) / target_std``;
    ``refined_mae_m`` reports the refined error back in metres."""
    is_training = optimizer is not None
    model.train(mode=is_training)

    total_loss = 0.0
    total_rough_loss = 0.0
    total_refined_loss = 0.0
    total_samples = 0

    progress = tqdm(data_loader, desc="train" if is_training else "val", leave=False, dynamic_ncols=True)
    for depth_data, robot_info, target_heightmap in progress:
        depth_data = depth_data.to(device)
        robot_info = robot_info.to(device)
        target_heightmap = (target_heightmap.to(device) - target_mean) / target_std

        if is_training:
            optimizer.zero_grad(set_to_none=True)

        with torch.set_grad_enabled(is_training):
            prediction = model(depth_data=depth_data, robot_info=robot_info)
            losses = compute_reconstruction_losses(
                prediction=prediction, target_heightmap=target_heightmap, rough_loss_type=rough_loss_type
            )

        if is_training:
            losses["loss"].backward()
            optimizer.step()

        batch_size = depth_data.shape[0]
        total_samples += batch_size
        total_loss += losses["loss"].item() * batch_size
        total_rough_loss += losses["rough_loss"].item() * batch_size
        total_refined_loss += losses["refined_loss"].item() * batch_size
        progress.set_postfix(loss=f"{total_loss / total_samples:.4f}")

    return {
        "loss": total_loss / max(total_samples, 1),
        "rough_loss": total_rough_loss / max(total_samples, 1),
        "refined_loss": total_refined_loss / max(total_samples, 1),
        "refined_mae_m": total_refined_loss / max(total_samples, 1) * target_std,
    }


def train_terrain_reconstructor(
    model: MultiModalTerrainReconstructor,
    train_loader: DataLoader,
    validation_loader: DataLoader | None = None,
    num_epochs: int = 5,
    learning_rate: float = 3e-4,
    weight_decay: float = 1e-4,
    device: str | torch.device = "cpu",
    epoch_callback: Callable[[dict[str, float]], None] | None = None,
    target_mean: float = 0.0,
    target_std: float = 1.0,
    rough_loss_type: str = "mse",
    lr_schedule: str = "constant",
    restore_best: bool = False,
) -> list[dict[str, float]]:
    """Train the reconstructor. With ``restore_best`` and a validation loader, the model ends with the weights
    of the epoch with the lowest validation refined loss instead of the last epoch."""
    device = torch.device(device)
    model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=weight_decay)
    if lr_schedule == "cosine":
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=num_epochs, eta_min=0.01 * learning_rate)
    elif lr_schedule == "constant":
        scheduler = None
    else:
        raise ValueError(f"Unknown lr_schedule: {lr_schedule}")
    epoch_kwargs = dict(target_mean=target_mean, target_std=target_std, rough_loss_type=rough_loss_type)

    best_val_loss = float("inf")
    best_state: dict[str, Tensor] | None = None
    history: list[dict[str, float]] = []
    for epoch in tqdm(range(num_epochs), desc="epochs", dynamic_ncols=True):
        current_lr = optimizer.param_groups[0]["lr"]
        train_metrics = _run_epoch(model=model, data_loader=train_loader, device=device, optimizer=optimizer, **epoch_kwargs)
        if scheduler is not None:
            scheduler.step()
        epoch_metrics = {
            "epoch": float(epoch + 1),
            "lr": current_lr,
            "train_loss": train_metrics["loss"],
            "train_rough_loss": train_metrics["rough_loss"],
            "train_refined_loss": train_metrics["refined_loss"],
            "train_refined_mae_m": train_metrics["refined_mae_m"],
        }

        if validation_loader is not None:
            with torch.no_grad():
                validation_metrics = _run_epoch(
                    model=model, data_loader=validation_loader, device=device, optimizer=None, **epoch_kwargs
                )
            epoch_metrics.update(
                {
                    "val_loss": validation_metrics["loss"],
                    "val_rough_loss": validation_metrics["rough_loss"],
                    "val_refined_loss": validation_metrics["refined_loss"],
                    "val_refined_mae_m": validation_metrics["refined_mae_m"],
                }
            )
            if restore_best and validation_metrics["refined_loss"] < best_val_loss:
                best_val_loss = validation_metrics["refined_loss"]
                best_state = {name: value.detach().cpu().clone() for name, value in model.state_dict().items()}

        history.append(epoch_metrics)
        if epoch_callback is not None:
            epoch_callback(epoch_metrics)

        summary = (
            f"Epoch {epoch + 1}/{num_epochs} | "
            f"train: total={epoch_metrics['train_loss']:.4f}, "
            f"rough={epoch_metrics['train_rough_loss']:.4f}, "
            f"refined={epoch_metrics['train_refined_loss']:.4f}"
        )
        if validation_loader is not None:
            summary += (
                f" | val: total={epoch_metrics['val_loss']:.4f}, "
                f"rough={epoch_metrics['val_rough_loss']:.4f}, "
                f"refined={epoch_metrics['val_refined_loss']:.4f}, "
                f"MAE={epoch_metrics['val_refined_mae_m'] * 1000:.2f} mm"
            )
        tqdm.write(summary)

    if best_state is not None:
        model.load_state_dict(best_state)
        best_epoch = min(history, key=lambda metrics: metrics["val_refined_loss"])["epoch"]
        tqdm.write(f"[INFO] Restored best weights from epoch {int(best_epoch)} (val refined loss {best_val_loss:.4f}).")

    return history



def run_terrain_reconstruction(
    path: str | Sequence[str],
    device: str | torch.device | None = None,
    batch_size: int = 32,
    num_epochs: int = 50,
    model_path: str | None = None,
    use_wandb: bool = False,
    wandb_project: str = "go2-locomotion",
    run_name: str | None = None,
    target_key: str = "heightmaps",
    num_workers: int = 0,
) -> None:
    dataset_paths = [Path(p).expanduser().resolve() for p in ([path] if isinstance(path, (str, Path)) else path)]
    for dataset_path in dataset_paths:
        if not dataset_path.is_file():
            raise FileNotFoundError(f"Path not found: {dataset_path}")
    # the first file sets the default output location; several files are trained on as one dataset
    dataset_path = dataset_paths[0]
    dataset_path_record = str(dataset_path) if len(dataset_paths) == 1 else [str(p) for p in dataset_paths]

    torch.manual_seed(0)
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    dataset = SavedTerrainReconstructionDataset(dataset_path=[str(p) for p in dataset_paths], target_key=target_key)
    train_size = int(0.8 * len(dataset))
    val_size = int(len(dataset) - train_size)
    train_dataset, valid_dataset = random_split(
        dataset=dataset,
        lengths=[train_size, val_size],
        generator=torch.Generator().manual_seed(0)
    )
    loader_kwargs = {"num_workers": num_workers, "persistent_workers": num_workers > 0}
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, **loader_kwargs)
    valid_loader = DataLoader(valid_dataset, batch_size=batch_size, shuffle=False, **loader_kwargs)

    model_config = {
        "proprio_dim": dataset.robot_info.shape[-1],
        "depth_channels": dataset.depth_data.shape[-3],
        "heightmap_size": tuple(dataset.heightmaps.shape[-2:]),
    }
    model = MultiModalTerrainReconstructor(**model_config)

    # Heights are in metres with millimetre-to-centimetre variations: train on standardized targets so the
    # losses and their gradients have a sensible scale. The model predicts normalized heights.
    train_heightmaps = dataset.heightmaps[train_dataset.indices]
    target_normalization = {
        "mean": train_heightmaps.mean().item(),
        "std": max(train_heightmaps.std().item(), 1e-6),
    }
    # MAE of always predicting the per-cell train mean: the model must beat this to be useful.
    baseline_mae = (dataset.heightmaps[valid_dataset.indices] - train_heightmaps.mean(dim=0, keepdim=True)).abs().mean().item()
    print(
        f"[INFO] Target normalization: mean={target_normalization['mean']:.4f} m, std={target_normalization['std']:.4f} m | "
        f"constant-prediction baseline val MAE: {baseline_mae * 1000:.2f} mm"
    )
    train_settings = {"rough_loss_type": "l1", "lr_schedule": "cosine", "restore_best": True}

    wandb_run = None
    epoch_callback = None
    if use_wandb:
        import wandb

        wandb_run = wandb.init(
            project=wandb_project,
            name=run_name,
            job_type="terrain_reconstruction",
            config={
                **model_config,
                "model": "transformer",
                "batch_size": batch_size,
                "num_epochs": num_epochs,
                "num_samples": len(dataset),
                "train_samples": train_size,
                "val_samples": val_size,
                "dataset_path": dataset_path_record,
                "target_key": target_key,
                "target_mean": target_normalization["mean"],
                "target_std": target_normalization["std"],
                **train_settings,
                **{f"dataset/{key}": value for key, value in dataset.metadata.items()},
            },
        )
        wandb_run.summary["val/constant_baseline_mae_m"] = baseline_mae

        def epoch_callback(metrics: dict[str, float]) -> None:
            # "train_rough_loss" -> "train/rough_loss", "val_loss" -> "val/loss"
            logged = {key.replace("_", "/", 1): value for key, value in metrics.items() if key != "epoch"}
            if "val_refined_mae_m" in metrics:
                logged["val/refined_mae_over_baseline"] = metrics["val_refined_mae_m"] / max(baseline_mae, 1e-12)
            wandb_run.log(logged, step=int(metrics["epoch"]))

    history = train_terrain_reconstructor(
        model=model,
        train_loader=train_loader,
        validation_loader=valid_loader,
        num_epochs=num_epochs,
        device=device,
        epoch_callback=epoch_callback,
        target_mean=target_normalization["mean"],
        target_std=target_normalization["std"],
        **train_settings,
    )
    best_metrics = min(history, key=lambda metrics: metrics["val_refined_loss"])

    output_path = Path(model_path) if model_path else dataset_path.with_name("transformer_terrain_reconstructor.pt")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "model_state_dict": {name: parameter.detach().cpu() for name, parameter in model.state_dict().items()},
            "model_config": model_config,
            # The model predicts normalized heights: heightmap_m = prediction * std + mean.
            "target_normalization": target_normalization,
            "train_settings": train_settings,
            "best_epoch": int(best_metrics["epoch"]),
            "dataset_path": dataset_path_record,
            "target_key": target_key,
            "dataset_metadata": dataset.metadata,
            "history": history,
        },
        output_path,
    )
    print(
        f"[INFO] Saved transformer model checkpoint (best epoch {int(best_metrics['epoch'])}, "
        f"val MAE {best_metrics['val_refined_mae_m'] * 1000:.2f} mm vs baseline {baseline_mae * 1000:.2f} mm) to: {output_path}"
    )

    # Split the validation error by terrain type: flat samples dominate the dataset and hide how the model
    # does on actual terrain.
    val_target, val_prediction = _predict_heightmaps(model, valid_loader, device, target_normalization)
    non_flat = val_target.flatten(1).std(dim=1) >= NON_FLAT_STD_THRESHOLD_M
    constant_prediction = train_heightmaps.mean(dim=0, keepdim=True)
    split_metrics = {}
    for split_name, mask in (("flat", ~non_flat), ("non_flat", non_flat)):
        if mask.any():
            split_metrics[f"val/{split_name}_mae_m"] = (val_prediction[mask] - val_target[mask]).abs().mean().item()
            split_metrics[f"val/{split_name}_constant_baseline_mae_m"] = (
                (constant_prediction - val_target[mask]).abs().mean().item()
            )
        split_metrics[f"val/{split_name}_samples"] = int(mask.sum().item())
    print(
        "[INFO] Val MAE by terrain | "
        + " | ".join(
            f"{split_name}: {split_metrics[f'val/{split_name}_mae_m'] * 1000:.2f} mm "
            f"(constant {split_metrics[f'val/{split_name}_constant_baseline_mae_m'] * 1000:.2f} mm, "
            f"n={split_metrics[f'val/{split_name}_samples']})"
            for split_name in ("flat", "non_flat")
            if f"val/{split_name}_mae_m" in split_metrics
        )
    )

    if wandb_run is not None:
        wandb_run.summary["best_epoch"] = int(best_metrics["epoch"])
        wandb_run.summary["best/val_refined_mae_m"] = best_metrics["val_refined_mae_m"]
        wandb_run.summary.update(split_metrics)
        wandb_run.log({"heightmaps": _heightmap_comparison_figure(val_target, val_prediction, non_flat)}, step=num_epochs)
        wandb_run.summary["model_path"] = str(output_path)
        wandb_run.finish()


# A heightmap whose cell heights vary by at least this much (standard deviation) counts as actual terrain.
NON_FLAT_STD_THRESHOLD_M = 0.01


def _predict_heightmaps(
    model: nn.Module,
    data_loader: DataLoader,
    device: str | torch.device,
    target_normalization: dict[str, float],
) -> tuple[Tensor, Tensor]:
    """Return (target, refined prediction) in metres for every sample of the loader, shaped (N, H, W)."""
    model.eval()
    targets, predictions = [], []
    with torch.no_grad():
        for depth_data, robot_info, target in data_loader:
            prediction = model(depth_data=depth_data.to(device), robot_info=robot_info.to(device)).refined_heightmap
            predictions.append(prediction.cpu()[:, 0] * target_normalization["std"] + target_normalization["mean"])
            targets.append(target[:, 0])
    return torch.cat(targets), torch.cat(predictions)


def _heightmap_comparison_figure(
    target: Tensor,
    prediction: Tensor,
    non_flat: Tensor,
    num_non_flat: int = 3,
    num_flat: int = 1,
    error_scale_mm: float = 30.0,
    min_height_span_mm: float = 20.0,
):
    """Plot target / prediction / |error| in millimetres for a few non-flat samples plus a flat reference.

    Target and prediction share a colour scale per row, spanning at least ``min_height_span_mm``; the error uses
    the same fixed scale in every row, so rows can be compared at a glance.
    """
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import wandb

    generator = torch.Generator().manual_seed(0)
    non_flat_ids = non_flat.nonzero().flatten()
    flat_ids = (~non_flat).nonzero().flatten()
    sample_ids = torch.cat(
        (
            non_flat_ids[torch.randperm(len(non_flat_ids), generator=generator)[:num_non_flat]],
            flat_ids[torch.randperm(len(flat_ids), generator=generator)[:num_flat]],
        )
    ).tolist()

    figure, axes = plt.subplots(len(sample_ids), 3, figsize=(7.5, 2.6 * len(sample_ids)), squeeze=False)
    for row, sample_id in enumerate(sample_ids):
        target_map, predicted_map = target[sample_id] * 1000, prediction[sample_id] * 1000
        vmin = min(target_map.min().item(), predicted_map.min().item())
        vmax = max(target_map.max().item(), predicted_map.max().item())
        # Enforce a minimum colour span: otherwise sub-millimetre noise on flat samples is stretched over the
        # whole colormap and looks like real terrain.
        if vmax - vmin < min_height_span_mm:
            center = 0.5 * (vmax + vmin)
            vmin, vmax = center - 0.5 * min_height_span_mm, center + 0.5 * min_height_span_mm
        kind = "non-flat" if non_flat[sample_id] else "flat"
        panels = (
            (target_map, f"target [mm] ({kind})", dict(vmin=vmin, vmax=vmax)),
            (predicted_map, "prediction [mm]", dict(vmin=vmin, vmax=vmax)),
            ((predicted_map - target_map).abs(), "|error| [mm]", dict(cmap="magma", vmin=0.0, vmax=error_scale_mm)),
        )
        for column, (image, title, kwargs) in enumerate(panels):
            axis = axes[row, column]
            figure.colorbar(axis.imshow(image.numpy(), **kwargs), ax=axis, fraction=0.046)
            axis.set_title(title, fontsize=9)
            axis.set_xticks([])
            axis.set_yticks([])
    figure.tight_layout()
    image = wandb.Image(figure)
    plt.close(figure)
    return image



def run_fake_data_smoke_test(
    device: str | torch.device | None = None,
    num_samples: int = 96,
    batch_size: int = 8,
    num_epochs: int = 3,
) -> None:
    torch.manual_seed(0)
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"

    dataset = FakeTerrainReconstructionDataset(num_samples=num_samples)
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = random_split(
        dataset,
        [train_size, val_size],
        generator=torch.Generator().manual_seed(0),
    )

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    model = MultiModalTerrainReconstructor(proprio_dim=dataset.robot_info.shape[-1])
    history = train_terrain_reconstructor(
        model=model,
        train_loader=train_loader,
        validation_loader=val_loader,
        num_epochs=num_epochs,
        device=device,
    )

    sample_depth, sample_robot_info, sample_target = next(iter(val_loader))
    sample_depth = sample_depth.to(device)
    sample_robot_info = sample_robot_info.to(device)
    sample_target = sample_target.to(device)

    model.eval()
    with torch.no_grad():
        sample_prediction = model(depth_data=sample_depth, robot_info=sample_robot_info)

    assert sample_prediction.rough_heightmap.shape == sample_target.shape
    assert sample_prediction.refined_heightmap.shape == sample_target.shape

    final_metrics = history[-1]
    print(
        "Smoke test passed | "
        f"depth={tuple(sample_depth.shape)}, "
        f"robot_info={tuple(sample_robot_info.shape)}, "
        f"heightmap={tuple(sample_prediction.refined_heightmap.shape)}, "
        f"final_val_loss={final_metrics.get('val_loss', final_metrics['train_loss']):.4f}"
    )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train the terrain reconstruction transformer.")
    parser.add_argument(
        "--dataset_path",
        type=str,
        nargs="+",
        default="logs/rsl_rl/rough_direct/2026-09-23_11-00-59_phase1_go2/terrain_reconstruction_dataset.pt",
        help=(
            "Path to a collected terrain_reconstruction_dataset.pt file, or several files trained on as one dataset."
            " If omitted, runs a fake-data smoke test."
        ),
    )
    parser.add_argument("--device", type=str, default=None, help="Training device. Defaults to cuda if available.")
    parser.add_argument("--num_samples", type=int, default=96, help="Number of fake samples.")
    parser.add_argument(
        "--batch_size",
        type=int,
        default=None,
        help="Training batch size. Defaults to 32 for saved datasets and 8 for fake-data smoke tests.",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=None,
        help="Number of training epochs. Defaults to 50 for saved datasets and 3 for fake-data smoke tests.",
    )
    parser.add_argument(
        "--model_path",
        type=str,
        default=None,
        help="Where to save the trained model. Defaults to <dataset_dir>/transformer_terrain_reconstructor.pt.",
    )
    parser.add_argument("--wandb", action="store_true", help="Log training metrics to Weights & Biases.")
    parser.add_argument("--wandb_project", type=str, default="go2-locomotion", help="W&B project name.")
    parser.add_argument("--run_name", type=str, default=None, help="W&B run name.")
    parser.add_argument(
        "--target_key",
        type=str,
        default="heightmaps",
        help="Dataset key of the target heightmaps, e.g. 'heightmaps_shifted' for the grid moved toward the camera.",
    )
    parser.add_argument(
        "--num_workers", type=int, default=0, help="DataLoader worker processes that read samples from disk."
    )
    return parser.parse_args()


__all__ = [
    "FakeTerrainReconstructionDataset",
    "MultiModalTerrainReconstructor",
    "SavedTerrainReconstructionDataset",
    "TerrainReconstructionOutput",
    "compute_reconstruction_losses",
    "run_fake_data_smoke_test",
    "run_terrain_reconstruction",
    "train_terrain_reconstructor",
]


if __name__ == "__main__":
    args = _parse_args()
    if args.dataset_path:
        run_terrain_reconstruction(
            path=args.dataset_path,
            device=args.device,
            batch_size=args.batch_size if args.batch_size is not None else 32,
            num_epochs=args.epochs if args.epochs is not None else 50,
            model_path=args.model_path,
            use_wandb=args.wandb,
            wandb_project=args.wandb_project,
            run_name=args.run_name,
            target_key=args.target_key,
            num_workers=args.num_workers,
        )
    else:
        run_fake_data_smoke_test(
            device=args.device,
            num_samples=args.num_samples,
            batch_size=args.batch_size if args.batch_size is not None else 8,
            num_epochs=args.epochs if args.epochs is not None else 3,
        )
