from __future__ import annotations

import argparse
import bisect
import glob
import math
import os
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path

import torch
import torch.nn.functional as F
from torch import Tensor, nn
from torch.utils.data import DataLoader, Dataset, RandomSampler, Subset, random_split
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
        context_from_newest_frame: bool = False,
    ):
        super().__init__()
        self.token_grid_size = token_grid_size
        self.context_from_newest_frame = context_from_newest_frame

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

    def encode_frames(self, frames: Tensor) -> Tensor:
        """(N, C, H, W) -> token maps (N, D, h, w). Each frame is encoded on its own, so a frame shared by several
        windows can be encoded once."""
        return self.token_projection(self.token_pool(self.encoder(frames)))

    def forward(self, depth_sequence: Tensor) -> tuple[Tensor, Tensor]:
        batch_size, depth_steps = depth_sequence.shape[:2]
        token_maps = self.encode_frames(depth_sequence.flatten(0, 1)).unflatten(0, (batch_size, depth_steps))
        return self.tokens_from_maps(token_maps)

    def tokens_from_maps(self, token_maps: Tensor) -> tuple[Tensor, Tensor]:
        batch_size, depth_steps = token_maps.shape[:2]
        token_grid_h, token_grid_w = self.token_grid_size
        #T: num of depth frame, D: embed_dim, H/W: frame size. token_maps: (B, T, D, H, W)

        depth_tokens = token_maps.permute(0, 1, 3, 4, 2).reshape(batch_size, depth_steps, token_grid_h * token_grid_w, -1)  # (B, T, H*W, D)
        time_pos = _sinusoidal_position_embedding(depth_steps, depth_tokens.shape[-1], depth_tokens.device, depth_tokens.dtype)
        spatial_pos = _sinusoidal_position_embedding(
            token_grid_h * token_grid_w, depth_tokens.shape[-1], depth_tokens.device, depth_tokens.dtype
        )
        depth_tokens = depth_tokens + time_pos.view(1, depth_steps, 1, -1) + spatial_pos.view(1, 1, token_grid_h * token_grid_w, -1)
        depth_tokens = self.token_norm(depth_tokens).reshape(batch_size, depth_steps * token_grid_h * token_grid_w, -1)  # (B, T*H*W, D)
        # Mean along dim=1 (B, T, D, H, W) -> (B, D, H, W). With a long depth stride the frames are far apart in time
        # and their mean is blurred, so the context can come from the newest frame alone (the last one).
        context_maps = token_maps[:, -1] if self.context_from_newest_frame else token_maps.mean(dim=1)
        depth_context = self.context_projection(context_maps)  #(B, context_channels, H, W)
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
        align_refiner_context: bool = False,
        recurrent_steps: bool = False,
        refiner_context_newest_frame: bool = False,
    ):
        super().__init__()
        self.heightmap_size = heightmap_size
        # Turn the image-space depth context into the heightmap layout before the refiner (see forward).
        # False keeps the original behaviour, so checkpoints trained without it still load and evaluate the same.
        self.align_refiner_context = align_refiner_context
        self.recurrent_steps = recurrent_steps

        self.depth_encoder = DepthTokenEncoder(
            depth_channels=depth_channels,
            embed_dim=embed_dim,
            token_grid_size=token_grid_size,
            context_channels=refinement_context_channels,
            context_from_newest_frame=refiner_context_newest_frame,
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
        if recurrent_steps:
            self.step_memory = nn.GRU(input_size=recurrent_hidden_dim, hidden_size=recurrent_hidden_dim, batch_first=True)
            self.step_memory_projection = nn.Linear(recurrent_hidden_dim, recurrent_hidden_dim)
            nn.init.zeros_(self.step_memory_projection.weight)
            nn.init.zeros_(self.step_memory_projection.bias)
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
        depth_index: Tensor | None = None,
    ) -> TerrainReconstructionOutput:
        """depth_data `(B, N, C, H, W)` holds the frames the windows share, depth_index `(L, T_depth)` picks each step's window
        and robot_info is `(B, L, T_prop, F)`; the outputs are then `(B, L, 1, h, w)`."""
        if depth_index is not None:
            batch_size, segment_length = robot_info.shape[:2]
            token_maps = self.depth_encoder.encode_frames(depth_data.flatten(0, 1)).unflatten(0, depth_data.shape[:2])
            token_maps = token_maps[:, depth_index].flatten(0, 1)  # (B * L, T_depth, D, h, w)
            proprio_history = robot_info.flatten(0, 1)
        else:
            depth_sequence = self._prepare_depth_sequence(depth_data)
            proprio_history = self._prepare_proprio_history(robot_info)
            batch_size, segment_length = depth_sequence.shape[0], 1
            token_maps = self.depth_encoder.encode_frames(depth_sequence.flatten(0, 1)).unflatten(0, depth_sequence.shape[:2])

        depth_tokens, depth_context = self.depth_encoder.tokens_from_maps(token_maps)
        proprio_tokens = self.proprio_encoder(proprio_history)

        fused_tokens = proprio_tokens
        for block in self.cross_attention_blocks:
            fused_tokens = block(fused_tokens, depth_tokens)

        memory_tokens, _ = self.memory(fused_tokens)
        step_feature = memory_tokens[:, -1]  # (B * L, recurrent_hidden_dim)
        if self.recurrent_steps:
            step_memory, hidden_state = self.step_memory(step_feature.view(batch_size, segment_length, -1), hidden_state)
            step_feature = step_feature + self.step_memory_projection(step_memory.flatten(0, 1))
        else:
            hidden_state = None
        rough_heightmap = self.rough_decoder(step_feature).view(-1, 1, *self.heightmap_size)#(B, 1, ?, ?)
        depth_context = self.refinement_context_projection(depth_context) ##(B, context_channels, H, W)
        #print(f"[FORWARD]: {rough_heightmap.shape=}", flush=True)
        #print(f"[FORWARD]: {depth_context.shape=}", flush=True)
        if self.align_refiner_context:
            # image rows = distance (top = far), image cols = lateral (left -> right); heightmap rows = lateral
            # (y from -0.4 = right to +0.4 = left), heightmap cols = distance (x from near to far)
            n_y, n_x = self.heightmap_size
            depth_context = F.interpolate(depth_context, size=(n_x, n_y), mode="bilinear", align_corners=False)
            depth_context = depth_context.transpose(-1, -2).flip(-2, -1)  # (B, C, n_y, n_x), same layout as the heightmap
        else:
            depth_context = F.interpolate(depth_context, size=self.heightmap_size, mode="bilinear", align_corners=False)
        #print(f"[FORWARD]: {depth_context.shape=}", flush=True)
        #exit(0)
        refinement_input = torch.cat((rough_heightmap, depth_context), dim=1)
        refinement_residual = self.refiner(refinement_input)
        refined_heightmap = rough_heightmap + refinement_residual
        if depth_index is not None:
            rough_heightmap = rough_heightmap.unflatten(0, (batch_size, segment_length))
            refined_heightmap = refined_heightmap.unflatten(0, (batch_size, segment_length))

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


class SequenceTerrainReconstructionDataset(Dataset):
    """Windows cut from the sequences of collect_depth_to_heightmap.py (one directory of chunk files per run).

    The chunks hold every step of every env once, time-major ``(steps, envs, ...)``, memory-mapped. A sample ending
    at step t of env e is built on access: depth frames t - (L_d - 1) * S, ..., t (length L_d, stride S), the last P
    'common' observations and the target at t, with the same shapes as ``SavedTerrainReconstructionDataset``. With
    ``segment_length`` L > 1 a sample is L consecutive steps of one env, for a memory carried across steps: the frames
    the L windows share ``(L + (L_d - 1) * S, C, H, W)``, the robot_info windows ``(L, P, F)``, the targets
    ``(L, 1, h, w)`` and ``depth_index`` ``(L, L_d)``, which picks each step's frames. No window crosses a reset: every
    step in t - K .. t + L - 1, with K = max((L_d - 1) * S, P - 1), must have ``dones`` False, which also drops the
    reset step itself.
    """

    def __init__(
        self,
        dataset_path: str | Sequence[str],
        target_key: str = "heightmaps",
        depth_history_length: int = 5,
        depth_history_stride: int = 1,
        proprio_history_length: int = 50,
        segment_length: int = 1,
    ):
        super().__init__()
        directories = [dataset_path] if isinstance(dataset_path, (str, Path)) else list(dataset_path)
        self.target_key = target_key
        self.segment_length = segment_length
        # window offsets relative to the sample step, oldest first
        self.depth_offsets = (torch.arange(depth_history_length) - (depth_history_length - 1)) * depth_history_stride
        self.proprio_offsets = torch.arange(proprio_history_length) - (proprio_history_length - 1)
        self.history = history = max(-int(self.depth_offsets[0]), -int(self.proprio_offsets[0]))
        # frames of each step's window, counted from the first frame the segment reads
        self.depth_index = torch.arange(segment_length).unsqueeze(1) + self.depth_offsets - int(self.depth_offsets[0])

        required_keys = {"depth_data", "robot_info", target_key, "dones"}
        self.runs: list[dict] = []
        index, targets = [], []
        for run, directory in enumerate(directories):
            paths = sorted(glob.glob(os.path.join(str(directory), "chunk_*.pt")))
            if not paths:
                raise FileNotFoundError(f"No chunk_*.pt files in {directory}")
            chunks = [torch.load(path, map_location="cpu", mmap=True, weights_only=True) for path in paths]
            for path, chunk in zip(paths, chunks):
                missing_keys = required_keys.difference(chunk)
                if missing_keys:
                    raise KeyError(f"Chunk {path} is missing required keys: {', '.join(sorted(missing_keys))}")
            starts = [0]
            for chunk in chunks:
                if chunk["metadata"]["first_step"] != starts[-1]:
                    raise ValueError(f"Chunks in {directory} are not consecutive: {paths}")
                starts.append(starts[-1] + chunk["dones"].shape[0])

            # resets[i] = number of resets in steps 0 .. i-1, so steps a .. b are clean if resets[b + 1] == resets[a]
            dones = torch.cat([chunk["dones"] for chunk in chunks])
            resets = torch.cat([torch.zeros(1, dones.shape[1], dtype=torch.long), dones.long().cumsum(dim=0)])
            first = torch.arange(history, dones.shape[0] - segment_length + 1)
            clean = resets[first + segment_length] == resets[first - history]
            sample_steps, sample_envs = clean.nonzero(as_tuple=True)
            sample_steps = first[sample_steps]
            index.append(torch.stack((torch.full_like(sample_steps, run), sample_steps, sample_envs), dim=1))
            # target at the last step of each sample: target statistics and baselines
            all_targets = torch.cat([chunk[target_key] for chunk in chunks])
            targets.append(all_targets[sample_steps + segment_length - 1, sample_envs].float())
            self.runs.append({"chunks": chunks, "starts": starts, "resets": resets})

        self.index = torch.cat(index)
        self.heightmaps = torch.cat(targets)
        # one id per (run, env): consecutive steps are near duplicates, so hold out whole envs for validation
        self.env_ids = self.index[:, 0] * 1_000_000 + self.index[:, 2]
        metadata = self.runs[0]["chunks"][0]["metadata"]
        self.metadata = {
            **{key: value for key, value in metadata.items()
               if not torch.is_tensor(value) and key not in ("chunk_index", "first_step", "num_steps")},
            "dataset_directories": [str(directory) for directory in directories],
            "depth_history_length": depth_history_length,
            "depth_history_stride": depth_history_stride,
            "proprio_history_length": proprio_history_length,
            "segment_length": segment_length,
        }

    def _rows(self, run: int, name: str, start: int, stop: int, env: int) -> Tensor:
        """Steps start .. stop-1 of one env, across chunk boundaries."""
        chunks, starts = self.runs[run]["chunks"], self.runs[run]["starts"]
        parts = []
        chunk = bisect.bisect_right(starts, start) - 1
        while start < stop:
            end = min(stop, starts[chunk + 1])
            parts.append(chunks[chunk][name][start - starts[chunk] : end - starts[chunk], env])
            start, chunk = end, chunk + 1
        return parts[0] if len(parts) == 1 else torch.cat(parts)

    def step_rows(self, run: int, name: str, step: int) -> Tensor:
        """One step of every env of a run: (envs, ...)."""
        chunks, starts = self.runs[run]["chunks"], self.runs[run]["starts"]
        chunk = bisect.bisect_right(starts, step) - 1
        return chunks[chunk][name][step - starts[chunk]]

    def __len__(self) -> int:
        return self.index.shape[0]

    def __getitem__(self, index: int) -> tuple[Tensor, ...]:
        run, first, env = self.index[index].tolist()
        stop = first + self.segment_length
        depth_start = first + int(self.depth_offsets[0])
        proprio_start = first + int(self.proprio_offsets[0])
        if self.segment_length == 1:  # only the L_d frames of the window, not the whole span between them
            depth = torch.stack([self._rows(run, "depth_data", first + offset, first + offset + 1, env)[0]
                                 for offset in self.depth_offsets.tolist()]).float()
        else:
            depth = self._rows(run, "depth_data", depth_start, stop, env).float()
        robot_info = self._rows(run, "robot_info", proprio_start, stop, env).float()
        target = self._rows(run, self.target_key, first, stop, env).float()
        # (L, window) row indices into the rows read above
        steps = torch.arange(self.segment_length).unsqueeze(1)
        robot_info = robot_info[steps + self.proprio_offsets - int(self.proprio_offsets[0])]
        if self.segment_length == 1:
            return depth, robot_info[0], target[0]
        return depth, robot_info, target, self.depth_index


def _load_dataset(
    path: str | Sequence[str], target_key: str, depth_history_stride: int, segment_length: int = 1
) -> Dataset:
    """Sequence directories -> SequenceTerrainReconstructionDataset, dataset files -> SavedTerrainReconstructionDataset."""
    paths = [path] if isinstance(path, (str, Path)) else list(path)
    if all(os.path.isdir(p) for p in paths):
        return SequenceTerrainReconstructionDataset(
            dataset_path=paths,
            target_key=target_key,
            depth_history_stride=depth_history_stride,
            segment_length=segment_length,
        )
    return SavedTerrainReconstructionDataset(dataset_path=paths, target_key=target_key)


def _segment_prediction(
    model: MultiModalTerrainReconstructor, depth_data: Tensor, robot_info: Tensor, depth_index: Tensor, burn_in: int
) -> TerrainReconstructionOutput:
    """Outputs on steps burn_in .. L-1 of a batch of segments. The burn-in steps only warm up the memory across steps
    (no loss, no gradient); a model without that memory skips them."""
    hidden_state = None
    if burn_in > 0 and model.recurrent_steps:
        with torch.no_grad():
            hidden_state = model(
                depth_data=depth_data[:, : int(depth_index[burn_in - 1, -1]) + 1],
                robot_info=robot_info[:, :burn_in],
                depth_index=depth_index[:burn_in],
            ).hidden_state
    # step s reads frames s + depth_index[0], so dropping the first burn_in frames shifts the index by burn_in
    return model(
        depth_data=depth_data[:, burn_in:],
        robot_info=robot_info[:, burn_in:],
        hidden_state=hidden_state,
        depth_index=depth_index[burn_in:] - burn_in,
    )


def _run_epoch(
    model: nn.Module,
    data_loader: DataLoader,
    device: torch.device,
    optimizer: torch.optim.Optimizer | None,
    target_mean: float = 0.0,
    target_std: float = 1.0,
    rough_loss_type: str = "mse",
    burn_in: int = 0,
    max_grad_norm: float | None = None,
) -> dict[str, float]:
    """Run one epoch. Losses are computed on normalized targets ``(target - target_mean) / target_std``;
    ``refined_mae_m`` reports the refined error back in metres. Batches of segments (a 4th element, depth_index) are
    scored on the steps after ``burn_in``, with truncated backpropagation through time over those steps."""
    is_training = optimizer is not None
    model.train(mode=is_training)

    total_loss = 0.0
    total_rough_loss = 0.0
    total_refined_loss = 0.0
    total_samples = 0

    progress = tqdm(data_loader, desc="train" if is_training else "val", leave=False, dynamic_ncols=True)
    for batch in progress:
        depth_data = batch[0].to(device)
        robot_info = batch[1].to(device)
        target_heightmap = (batch[2].to(device) - target_mean) / target_std

        if is_training:
            optimizer.zero_grad(set_to_none=True)

        with torch.set_grad_enabled(is_training):
            if len(batch) == 4:
                depth_index = batch[3][0].to(device)  # the same for every segment
                prediction = _segment_prediction(model, depth_data, robot_info, depth_index, burn_in)
                target_heightmap = target_heightmap[:, burn_in:]
            else:
                prediction = model(depth_data=depth_data, robot_info=robot_info)
            losses = compute_reconstruction_losses(
                prediction=prediction, target_heightmap=target_heightmap, rough_loss_type=rough_loss_type
            )

        if is_training:
            losses["loss"].backward()
            if max_grad_norm is not None:
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_grad_norm)
            optimizer.step()

        batch_size = target_heightmap.numel() // target_heightmap.shape[-3:].numel()  # heightmaps scored
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
    burn_in: int = 0,
    max_grad_norm: float | None = None,
    resume_path: str | Path | None = None,
    resume_info: dict | None = None,
) -> list[dict[str, float]]:
    """Train the reconstructor. With ``restore_best`` and a validation loader, the model ends with the weights
    of the epoch with the lowest validation refined loss instead of the last epoch. With ``resume_path`` the training
    state is saved there after every epoch (with ``resume_info``), and an existing file is continued from."""
    device = torch.device(device)
    model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=weight_decay)
    if lr_schedule == "cosine":
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=num_epochs, eta_min=0.01 * learning_rate)
    elif lr_schedule == "constant":
        scheduler = None
    else:
        raise ValueError(f"Unknown lr_schedule: {lr_schedule}")
    epoch_kwargs = dict(
        target_mean=target_mean,
        target_std=target_std,
        rough_loss_type=rough_loss_type,
        burn_in=burn_in,
        max_grad_norm=max_grad_norm,
    )

    best_val_loss = float("inf")
    best_state: dict[str, Tensor] | None = None
    history: list[dict[str, float]] = []
    if resume_path is not None and os.path.exists(resume_path):
        # an interrupted training: continue after its last finished epoch
        resume = torch.load(resume_path, map_location="cpu", weights_only=False)
        model.load_state_dict(resume["model"])
        optimizer.load_state_dict(resume["optimizer"])
        if scheduler is not None:
            scheduler.load_state_dict(resume["scheduler"])
        history, best_val_loss, best_state = resume["history"], resume["best_val_loss"], resume["best_state"]
        tqdm.write(f"[INFO] Resuming from {resume_path} after epoch {len(history)}/{num_epochs}.")
    first_epoch = len(history)
    for epoch in tqdm(range(first_epoch, num_epochs), desc="epochs", initial=first_epoch, total=num_epochs, dynamic_ncols=True):
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
        if resume_path is not None:
            state = {
                "model": model.state_dict(),
                "optimizer": optimizer.state_dict(),
                "scheduler": scheduler.state_dict() if scheduler is not None else None,
                "history": history,
                "best_val_loss": best_val_loss,
                "best_state": best_state,
                "info": resume_info,
            }
            torch.save(state, f"{resume_path}.tmp")
            os.replace(f"{resume_path}.tmp", resume_path)  # never leave a half-written file

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
    align_refiner_context: bool = False,
    test_dataset_path: str | Sequence[str] | None = None,
    depth_history_stride: int = 1,
    segment_length: int = 1,
    burn_in: int = 0,
    recurrent_steps: bool = False,
    samples_per_epoch: int | None = None,
    max_val_samples: int | None = None,
    refiner_context_newest_frame: bool = False,
    init_checkpoint: str | None = None,
    learning_rate: float = 3e-4,
) -> None:
    dataset_paths = [Path(p).expanduser().resolve() for p in ([path] if isinstance(path, (str, Path)) else path)]
    for dataset_path in dataset_paths:
        if not dataset_path.exists():
            raise FileNotFoundError(f"Path not found: {dataset_path}")
    # the first file sets the default output location; several files are trained on as one dataset
    dataset_path = dataset_paths[0]
    dataset_path_record = str(dataset_path) if len(dataset_paths) == 1 else [str(p) for p in dataset_paths]

    torch.manual_seed(0)
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    dataset = _load_dataset([str(p) for p in dataset_paths], target_key, depth_history_stride, segment_length)
    if isinstance(dataset, SequenceTerrainReconstructionDataset):
        # consecutive steps are near duplicates: validate on whole envs never seen in training
        is_valid = dataset.env_ids % 5 == 4
        train_ids, valid_ids = (~is_valid).nonzero().flatten(), is_valid.nonzero().flatten()
        if max_val_samples is not None and len(valid_ids) > max_val_samples:
            # overlapping windows of the same envs: a fixed random subset ranks the epochs just as well
            subset = torch.randperm(len(valid_ids), generator=torch.Generator().manual_seed(0))[:max_val_samples]
            valid_ids = valid_ids[subset.sort().values]
        train_dataset = Subset(dataset, train_ids.tolist())
        valid_dataset = Subset(dataset, valid_ids.tolist())
    else:
        train_size = int(0.8 * len(dataset))
        train_dataset, valid_dataset = random_split(
            dataset=dataset,
            lengths=[train_size, len(dataset) - train_size],
            generator=torch.Generator().manual_seed(0)
        )
    train_size, val_size = len(train_dataset), len(valid_dataset)
    loader_kwargs = {"num_workers": num_workers, "persistent_workers": num_workers > 0}
    # an epoch of samples_per_epoch random samples (all of them if None), different ones every epoch
    train_sampler = RandomSampler(train_dataset, num_samples=samples_per_epoch) if samples_per_epoch else None
    train_loader = DataLoader(
        train_dataset, batch_size=batch_size, shuffle=train_sampler is None, sampler=train_sampler, **loader_kwargs
    )
    valid_loader = DataLoader(valid_dataset, batch_size=batch_size, shuffle=False, **loader_kwargs)

    sample_depth, sample_robot_info, sample_target = dataset[0][:3]
    model_config = {
        "proprio_dim": sample_robot_info.shape[-1],
        "depth_channels": sample_depth.shape[-3],
        "heightmap_size": tuple(sample_target.shape[-2:]),
        "align_refiner_context": align_refiner_context,
        "recurrent_steps": recurrent_steps,
        "refiner_context_newest_frame": refiner_context_newest_frame,
    }

    train_heightmaps = dataset.heightmaps[train_dataset.indices]
    target_normalization = {
        "mean": train_heightmaps.mean().item(),
        "std": max(train_heightmaps.std().item(), 1e-6),
    }
    if init_checkpoint:
        # continue from a trained model, e.g. one without memory to add it: its architecture flags and weights (a new
        # memory across steps starts at zero), and its normalization, so its outputs keep their meaning
        init = torch.load(init_checkpoint, map_location="cpu", weights_only=False)
        model_config = {**init["model_config"], "recurrent_steps": recurrent_steps}
        target_normalization = init["target_normalization"]
    model = MultiModalTerrainReconstructor(**model_config)
    if init_checkpoint:
        missing, unexpected = model.load_state_dict(init["model_state_dict"], strict=False)
        if unexpected or any(not key.startswith("step_memory") for key in missing):
            raise ValueError(f"{init_checkpoint} does not match the model: missing {missing}, unexpected {unexpected}")
        print(f"[INFO] Initialised from {init_checkpoint}" + (f", new memory across steps ({len(missing)} tensors)" if missing else ""))
    # MAE of always predicting the per-cell train mean: the model must beat this to be useful.
    baseline_mae = (dataset.heightmaps[valid_dataset.indices] - train_heightmaps.mean(dim=0, keepdim=True)).abs().mean().item()
    print(
        f"[INFO] Target normalization: mean={target_normalization['mean']:.4f} m, std={target_normalization['std']:.4f} m | "
        f"constant-prediction baseline val MAE: {baseline_mae * 1000:.2f} mm"
    )
    train_settings = {"rough_loss_type": "l1", "lr_schedule": "cosine", "restore_best": True, "learning_rate": learning_rate}
    if segment_length > 1:
        train_settings.update(burn_in=burn_in, max_grad_norm=1.0)

    output_path = Path(model_path) if model_path else dataset_path.with_name("transformer_terrain_reconstructor.pt")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    # training state after every epoch: rerunning the same command after an interruption continues from it
    resume_path = output_path.with_suffix(".resume.pt")
    run_setup = {"model_config": model_config, "train_settings": train_settings, "num_epochs": num_epochs,
                 "batch_size": batch_size, "samples_per_epoch": samples_per_epoch, "dataset_path": dataset_path_record}
    resume_info = {"setup": run_setup}
    if resume_path.exists():
        previous = torch.load(resume_path, map_location="cpu", weights_only=False)["info"]
        if previous["setup"] != run_setup:
            raise ValueError(f"{resume_path} is from a different setup: delete it to start over.")
        resume_info = previous

    wandb_run = None
    epoch_callback = None
    if use_wandb:
        import wandb

        wandb_run = wandb.init(
            project=wandb_project,
            name=run_name,
            job_type="terrain_reconstruction",
            id=resume_info.get("wandb_id"),
            resume="allow",
            config={
                **model_config,
                "model": "transformer",
                "batch_size": batch_size,
                "num_epochs": num_epochs,
                "num_samples": len(dataset),
                "train_samples": train_size,
                "val_samples": val_size,
                "samples_per_epoch": samples_per_epoch or train_size,
                "init_checkpoint": init_checkpoint,
                "dataset_path": dataset_path_record,
                "target_key": target_key,
                "target_mean": target_normalization["mean"],
                "target_std": target_normalization["std"],
                **train_settings,
                **{f"dataset/{key}": value for key, value in dataset.metadata.items()},
            },
        )
        wandb_run.summary["val/constant_baseline_mae_m"] = baseline_mae
        resume_info["wandb_id"] = wandb_run.id

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
        resume_path=resume_path,
        resume_info=resume_info,
        **train_settings,
    )
    best_metrics = min(history, key=lambda metrics: metrics["val_refined_loss"])

    # Independent test set (other seed: new terrain and trajectories). The random validation split shares nearby
    # timesteps with training and is optimistic, the refiner even more so.
    test_metrics = {}
    if test_dataset_path:
        test_dataset = _load_dataset(test_dataset_path, target_key, depth_history_stride)
        train_stride = dataset.metadata.get("depth_history_stride")
        test_stride = test_dataset.metadata.get("depth_history_stride")
        if train_stride != test_stride:
            raise ValueError(f"Test set depth stride {test_stride} differs from the training set stride {train_stride}.")
        if isinstance(test_dataset, SequenceTerrainReconstructionDataset):
            # step by step through the recorded episodes, as on the robot, carrying the memory across steps
            def predict_test() -> dict[str, Tensor]:
                return _predict_rollouts(model, test_dataset, device, target_normalization)
        else:
            test_loader = DataLoader(test_dataset, batch_size=4 * batch_size, shuffle=False, num_workers=num_workers)

            def predict_test() -> dict[str, Tensor]:
                return _predict(model, test_loader, device, target_normalization)
        test_metrics = _evaluate_refiner_breakdown(model, predict_test)
        print(
            f"[INFO] Test MAE {test_metrics['test/mae_m'] * 1000:.2f} mm (non-flat {test_metrics['test/non_flat_mae_m'] * 1000:.2f}, "
            f"flat {test_metrics['test/flat_mae_m'] * 1000:.2f}, n={len(test_dataset)}) | refiner: rough alone "
            f"{test_metrics['test/rough_mae_m'] * 1000:.2f} mm, gain {test_metrics['test/refiner_gain_m'] * 1000:+.2f} mm, "
            f"of which from the image {test_metrics['test/refiner_image_gain_m'] * 1000:+.2f} mm"
        )
        age_metrics = [(key, value) for key, value in test_metrics.items() if key.startswith("test/mae_age")]
        if age_metrics:
            print("[INFO] Test MAE by memory age (steps) | " + " | ".join(
                f"{key[len('test/mae_age'):-2]}: {value * 1000:.2f} mm" for key, value in age_metrics))

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
            "test_dataset_path": test_dataset_path,
            "init_checkpoint": init_checkpoint,
            "test_metrics": test_metrics,
        },
        output_path,
    )
    resume_path.unlink(missing_ok=True)  # the training is complete: a rerun must start over, not resume
    print(
        f"[INFO] Saved transformer model checkpoint (best epoch {int(best_metrics['epoch'])}, "
        f"val MAE {best_metrics['val_refined_mae_m'] * 1000:.2f} mm vs baseline {baseline_mae * 1000:.2f} mm) to: {output_path}"
    )

    # Split the validation error by terrain type: flat samples dominate the dataset and hide how the model
    # does on actual terrain.
    val_predictions = _predict(model, valid_loader, device, target_normalization, train_settings.get("burn_in", 0))
    val_target, val_prediction = val_predictions["target"], val_predictions["refined"]
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
        wandb_run.summary.update(test_metrics)
        wandb_run.summary["model_path"] = str(output_path)
        wandb_run.finish()


# A heightmap whose cell heights vary by at least this much (standard deviation) counts as actual terrain.
NON_FLAT_STD_THRESHOLD_M = 0.01


def heightmap_error_summary(ground_error: Tensor) -> dict[str, float]:
    """A few numbers for a set of predicted heightmaps. ``ground_error`` is (steps, rows, cols): predicted minus true
    ground height in metres (> 0 = ground drawn too high, a drop that is missed). Columns run along x ahead of the base;
    the first three (x <= 0.3 m) are not in the current image of the D435 camera."""
    error = ground_error.abs()
    per_step_off = (error > 0.05).flatten(1).any(dim=1)
    return {
        "steps": int(error.shape[0]),
        "mae_mm": error.mean().item() * 1000,
        "mae_near_x_le_0.3m_mm": error[..., :3].mean().item() * 1000,
        "mae_far_x_ge_0.4m_mm": error[..., 3:].mean().item() * 1000,
        "cells_within_1cm_pct": (error < 0.01).float().mean().item() * 100,
        "cells_within_3cm_pct": (error < 0.03).float().mean().item() * 100,
        "cells_too_high_5cm_pct": (ground_error > 0.05).float().mean().item() * 100,
        "cells_too_low_5cm_pct": (ground_error < -0.05).float().mean().item() * 100,
        "steps_with_a_cell_off_5cm_pct": per_step_off.float().mean().item() * 100,
    }


# memory age bins (steps the memory across steps had already seen) for the rollout test metrics
MEMORY_AGE_BINS = ((0, 10), (10, 25), (25, 50), (50, 100), (100, 200), (200, 100_000))


def _evaluate_refiner_breakdown(
    model: MultiModalTerrainReconstructor, predict: Callable[[], dict[str, Tensor]]
) -> dict[str, float]:
    """Test metrics in metres, plus how much the refiner adds and how much of it comes from the depth image.

    ``predict`` returns the rough and refined predictions and the targets in metres (``_predict`` or
    ``_predict_rollouts``). Two passes: the model as trained (collecting the mean image context), then again with the
    image context of every sample replaced by that mean, so the refiner keeps its input statistics but loses the
    sample-specific image.
    """
    state = {"use_mean": False, "sum": 0.0, "count": 0}

    def context_hook(module, inputs, output):
        if state["use_mean"]:
            return (state["sum"] / state["count"]).expand_as(output)
        state["sum"] = state["sum"] + output.sum(dim=0, keepdim=True)
        state["count"] += output.shape[0]
        return output

    handle = model.refinement_context_projection.register_forward_hook(context_hook)
    try:
        result = predict()
        state["use_mean"] = True
        refined_mean_context = predict()["refined"]
    finally:
        handle.remove()
    rough, refined, target = result["rough"], result["refined"], result["target"]

    error = (refined - target).abs()
    non_flat = target.flatten(1).std(dim=1) >= NON_FLAT_STD_THRESHOLD_M
    rough_mae = (rough - target).abs().mean().item()
    mean_context_mae = (refined_mean_context - target).abs().mean().item()
    metrics = {
        "test/mae_m": error.mean().item(),
        "test/non_flat_mae_m": error[non_flat].mean().item() if non_flat.any() else float("nan"),
        "test/flat_mae_m": error[~non_flat].mean().item() if (~non_flat).any() else float("nan"),
        "test/rough_mae_m": rough_mae,
        "test/mean_image_context_mae_m": mean_context_mae,
        "test/refiner_gain_m": rough_mae - error.mean().item(),
        "test/refiner_image_gain_m": mean_context_mae - error.mean().item(),
        "test/samples": int(len(target)),
    }
    # non-flat error per heightmap column (x ahead of the base); the near columns are the ones the camera cannot see
    if non_flat.any():
        for column, column_error in enumerate(error[non_flat].mean(dim=(0, 1)).tolist()):
            metrics[f"test/non_flat_mae_col{column}_m"] = column_error
    if "age" in result:
        for low, high in MEMORY_AGE_BINS:
            in_bin = (result["age"] >= low) & (result["age"] < high)
            if in_bin.any():
                metrics[f"test/mae_age{low}-{high if high < 100_000 else 'inf'}_m"] = error[in_bin].mean().item()
    return metrics


def _predict(
    model: MultiModalTerrainReconstructor,
    data_loader: DataLoader,
    device: str | torch.device,
    target_normalization: dict[str, float],
    burn_in: int = 0,
) -> dict[str, Tensor]:
    """Rough and refined predictions and targets in metres, (N, h, w), for every sample of the loader (for batches of
    segments, every step after ``burn_in``)."""
    mean, std = target_normalization["mean"], target_normalization["std"]
    outputs = {"rough": [], "refined": [], "target": []}
    model.eval()
    with torch.no_grad():
        for batch in data_loader:
            depth_data, robot_info, target = batch[0].to(device), batch[1].to(device), batch[2]
            if len(batch) == 4:
                prediction = _segment_prediction(model, depth_data, robot_info, batch[3][0].to(device), burn_in)
                target = target[:, burn_in:]
            else:
                prediction = model(depth_data=depth_data, robot_info=robot_info)
            heightmap_size = target.shape[-2:]
            outputs["rough"].append(prediction.rough_heightmap.cpu().reshape(-1, *heightmap_size) * std + mean)
            outputs["refined"].append(prediction.refined_heightmap.cpu().reshape(-1, *heightmap_size) * std + mean)
            outputs["target"].append(target.reshape(-1, *heightmap_size))
    return {key: torch.cat(value) for key, value in outputs.items()}


def _predict_heightmaps(
    model: nn.Module,
    data_loader: DataLoader,
    device: str | torch.device,
    target_normalization: dict[str, float],
) -> tuple[Tensor, Tensor]:
    """Return (target, refined prediction) in metres for every sample of the loader, shaped (N, H, W)."""
    outputs = _predict(model, data_loader, device, target_normalization)
    return outputs["target"], outputs["refined"]


def _predict_rollouts(
    model: MultiModalTerrainReconstructor,
    dataset: SequenceTerrainReconstructionDataset,
    device: str | torch.device,
    target_normalization: dict[str, float],
) -> dict[str, Tensor]:
    """Predictions through every recorded step in order, as on the robot: all envs of a run at once, the memory across
    steps carried from one step to the next and restarted at the first clean window after a reset.

    Returns rough, refined and target in metres (N, h, w) on the steps with a clean window, with their run, step, env
    and memory age (N,): the number of steps the memory had already seen, 0 at its restart.
    """
    mean, std = target_normalization["mean"], target_normalization["std"]
    outputs = {key: [] for key in ("rough", "refined", "target", "run", "step", "env", "age")}
    model.eval()
    with torch.no_grad():
        for run, record in enumerate(dataset.runs):
            resets = record["resets"]
            robot_info = torch.cat([chunk["robot_info"] for chunk in record["chunks"]]).to(device)  # (steps, envs, F)
            frames: dict[int, Tensor] = {}  # depth frames on the device, kept while a window still needs them
            age = torch.full((resets.shape[1],), -1)
            hidden_state = None
            for step in range(dataset.history, resets.shape[0] - 1):
                clean = resets[step + 1] == resets[step - dataset.history]
                age = torch.where(clean, age + 1, -1)
                if hidden_state is not None:
                    restart = (age == 0).to(device).view(1, -1, 1)
                    hidden_state = torch.where(restart, torch.zeros_like(hidden_state), hidden_state)

                depth_steps = (step + dataset.depth_offsets).tolist()
                for old_step in [s for s in frames if s < depth_steps[0]]:
                    del frames[old_step]
                for depth_step in depth_steps:
                    if depth_step not in frames:
                        frames[depth_step] = dataset.step_rows(run, "depth_data", depth_step).to(device)
                prediction = model(
                    depth_data=torch.stack([frames[s] for s in depth_steps], dim=1).float(),
                    robot_info=robot_info[step + dataset.proprio_offsets].transpose(0, 1).float(),
                    hidden_state=hidden_state,
                )
                hidden_state = prediction.hidden_state

                envs = clean.nonzero().flatten()
                outputs["rough"].append(prediction.rough_heightmap[envs.to(device), 0].cpu() * std + mean)
                outputs["refined"].append(prediction.refined_heightmap[envs.to(device), 0].cpu() * std + mean)
                outputs["target"].append(dataset.step_rows(run, dataset.target_key, step)[envs, 0].float())
                outputs["run"].append(torch.full_like(envs, run))
                outputs["step"].append(torch.full_like(envs, step))
                outputs["env"].append(envs)
                outputs["age"].append(age[envs])
    return {key: torch.cat(value) for key, value in outputs.items()}


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
    parser.add_argument(
        "--align_refiner_context",
        action="store_true",
        help="Rotate the depth context into the heightmap layout (rows = lateral, cols = distance) before the refiner.",
    )
    parser.add_argument(
        "--depth_history_stride",
        type=int,
        default=1,
        help="Sequence datasets only: steps between the 5 depth frames of a sample (1 -> 80 ms, 10 -> 0.8 s).",
    )
    parser.add_argument(
        "--segment_length",
        type=int,
        default=1,
        help="Sequence datasets only: train on segments of this many consecutive steps of one env (> 1 for --recurrent_steps).",
    )
    parser.add_argument(
        "--burn_in", type=int, default=0, help="First steps of each segment: memory warm-up only, no loss and no gradient."
    )
    parser.add_argument(
        "--recurrent_steps", action="store_true", help="Add the memory carried across control steps (a second GRU)."
    )
    parser.add_argument(
        "--samples_per_epoch", type=int, default=None, help="Random training samples (segments) per epoch; default all."
    )
    parser.add_argument(
        "--max_val_samples", type=int, default=None, help="Sequence datasets only: fixed random subset of validation samples."
    )
    parser.add_argument(
        "--refiner_context_newest_frame",
        action="store_true",
        help="Refiner image context from the newest depth frame instead of the mean of all frames.",
    )
    parser.add_argument(
        "--init_checkpoint",
        type=str,
        default=None,
        help="Start from this trained checkpoint (its architecture, weights and normalization); with --recurrent_steps the memory is added.",
    )
    parser.add_argument("--learning_rate", type=float, default=3e-4, help="Peak learning rate (cosine schedule).")
    parser.add_argument(
        "--test_dataset_path",
        type=str,
        nargs="+",
        default=None,
        help="Independent test set(s), collected with another seed and the same depth stride, scored after training.",
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
    if isinstance(args.dataset_path, list):
        args.dataset_path = [path for path in args.dataset_path if path]  # --dataset_path "" runs the smoke test
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
            align_refiner_context=args.align_refiner_context,
            test_dataset_path=args.test_dataset_path,
            depth_history_stride=args.depth_history_stride,
            segment_length=args.segment_length,
            burn_in=args.burn_in,
            recurrent_steps=args.recurrent_steps,
            samples_per_epoch=args.samples_per_epoch,
            max_val_samples=args.max_val_samples,
            refiner_context_newest_frame=args.refiner_context_newest_frame,
            init_checkpoint=args.init_checkpoint,
            learning_rate=args.learning_rate,
        )
    else:
        run_fake_data_smoke_test(
            device=args.device,
            num_samples=args.num_samples,
            batch_size=args.batch_size if args.batch_size is not None else 8,
            num_epochs=args.epochs if args.epochs is not None else 3,
        )
