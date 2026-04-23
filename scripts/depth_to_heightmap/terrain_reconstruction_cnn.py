from __future__ import annotations

import argparse

import torch
import torch.nn.functional as F
from torch import Tensor, nn
from torch.utils.data import DataLoader, random_split

from terrain_reconstruction_transformer import (
    ConditionalUNetRefiner,
    ConvNormAct,
    FakeTerrainReconstructionDataset,
    ProprioceptiveHistoryEncoder,
    TerrainReconstructionOutput,
    compute_reconstruction_losses,
    train_terrain_reconstructor,
)


class DepthFeatureEncoder(nn.Module):
    def __init__(self, depth_channels: int, feature_dim: int, context_channels: int):
        super().__init__()
        self.backbone = nn.Sequential(
            ConvNormAct(depth_channels, 32, kernel_size=5, stride=2, padding=2),
            ConvNormAct(32, 64, kernel_size=3, stride=2, padding=1),
            ConvNormAct(64, 96, kernel_size=3, stride=2, padding=1),
            ConvNormAct(96, 128, kernel_size=3, padding=1),
        )
        self.sequence_pool = nn.AdaptiveAvgPool2d((4, 4))
        self.feature_projection = nn.Sequential(
            nn.Flatten(start_dim=1),
            nn.Linear(128 * 4 * 4, feature_dim),
            nn.GELU(),
        )
        self.context_projection = nn.Sequential(
            nn.Conv2d(128, context_channels, kernel_size=1),
            nn.GELU(),
        )

    def forward(self, depth_sequence: Tensor) -> tuple[Tensor, Tensor]:
        batch_size, depth_steps, channels, _, _ = depth_sequence.shape
        encoded = self.backbone(depth_sequence.reshape(batch_size * depth_steps, channels, *depth_sequence.shape[-2:]))

        sequence_features = self.feature_projection(self.sequence_pool(encoded))
        sequence_features = sequence_features.view(batch_size, depth_steps, -1)

        depth_context = self.context_projection(encoded)
        depth_context = depth_context.view(batch_size, depth_steps, depth_context.shape[1], *depth_context.shape[-2:]).mean(dim=1)
        return sequence_features, depth_context


class CNNGRUTerrainReconstructor(nn.Module):
    """Terrain reconstructor baseline with CNN encoders and GRU fusion, without attention."""

    def __init__(
        self,
        proprio_dim: int,
        depth_channels: int = 1,
        heightmap_size: tuple[int, int] = (20, 20),
        depth_feature_dim: int = 128,
        proprio_feature_dim: int = 128,
        proprio_hidden_dim: int = 256,
        depth_gru_hidden_dim: int = 128,
        proprio_gru_hidden_dim: int = 128,
        recurrent_layers: int = 1,
        fusion_hidden_dim: int = 256,
        refinement_context_channels: int = 32,
        refinement_base_channels: int = 32,
        dropout: float = 0.1,
    ):
        super().__init__()
        self.heightmap_size = heightmap_size
        self.depth_gru_hidden_dim = depth_gru_hidden_dim
        self.proprio_gru_hidden_dim = proprio_gru_hidden_dim

        self.depth_encoder = DepthFeatureEncoder(
            depth_channels=depth_channels,
            feature_dim=depth_feature_dim,
            context_channels=refinement_context_channels,
        )
        self.proprio_encoder = ProprioceptiveHistoryEncoder(
            proprio_dim=proprio_dim,
            embed_dim=proprio_feature_dim,
            hidden_dim=proprio_hidden_dim,
        )

        self.depth_memory = nn.GRU(
            input_size=depth_feature_dim,
            hidden_size=depth_gru_hidden_dim,
            num_layers=recurrent_layers,
            batch_first=True,
            dropout=dropout if recurrent_layers > 1 else 0.0,
        )
        self.proprio_memory = nn.GRU(
            input_size=proprio_feature_dim,
            hidden_size=proprio_gru_hidden_dim,
            num_layers=recurrent_layers,
            batch_first=True,
            dropout=dropout if recurrent_layers > 1 else 0.0,
        )

        fused_dim = depth_gru_hidden_dim + proprio_gru_hidden_dim
        self.rough_decoder = nn.Sequential(
            nn.LayerNorm(fused_dim),
            nn.Linear(fused_dim, fusion_hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(fusion_hidden_dim, heightmap_size[0] * heightmap_size[1]),
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

        if hidden_state is None:
            depth_hidden_state = None
            proprio_hidden_state = None
        else:
            depth_hidden_state = hidden_state[..., : self.depth_gru_hidden_dim].contiguous()
            proprio_hidden_state = hidden_state[..., self.depth_gru_hidden_dim :].contiguous()

        depth_features, depth_context = self.depth_encoder(depth_sequence)
        proprio_features = self.proprio_encoder(proprio_history)

        depth_memory_tokens, depth_hidden_state = self.depth_memory(depth_features, depth_hidden_state)
        proprio_memory_tokens, proprio_hidden_state = self.proprio_memory(proprio_features, proprio_hidden_state)

        fused_state = torch.cat((depth_memory_tokens[:, -1], proprio_memory_tokens[:, -1]), dim=-1)
        rough_heightmap = self.rough_decoder(fused_state).view(-1, 1, *self.heightmap_size)

        depth_context = self.refinement_context_projection(depth_context)
        depth_context = F.interpolate(depth_context, size=self.heightmap_size, mode="bilinear", align_corners=False)

        refinement_input = torch.cat((rough_heightmap, depth_context), dim=1)
        refinement_residual = self.refiner(refinement_input)
        refined_heightmap = rough_heightmap + refinement_residual

        stacked_hidden = torch.cat((depth_hidden_state, proprio_hidden_state), dim=-1)
        return TerrainReconstructionOutput(
            rough_heightmap=rough_heightmap,
            refined_heightmap=refined_heightmap,
            hidden_state=stacked_hidden,
        )


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

    model = CNNGRUTerrainReconstructor(proprio_dim=dataset.robot_info.shape[-1])
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
        losses = compute_reconstruction_losses(prediction=sample_prediction, target_heightmap=sample_target)

    assert sample_prediction.rough_heightmap.shape == sample_target.shape
    assert sample_prediction.refined_heightmap.shape == sample_target.shape

    final_metrics = history[-1]
    print(
        "CNN-GRU smoke test passed | "
        f"depth={tuple(sample_depth.shape)}, "
        f"robot_info={tuple(sample_robot_info.shape)}, "
        f"heightmap={tuple(sample_prediction.refined_heightmap.shape)}, "
        f"eval_loss={losses['loss'].item():.4f}, "
        f"final_val_loss={final_metrics.get('val_loss', final_metrics['train_loss']):.4f}"
    )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fake-data smoke test for the CNN-GRU terrain reconstructor.")
    parser.add_argument("--device", type=str, default=None, help="Training device. Defaults to cuda if available.")
    parser.add_argument("--num_samples", type=int, default=96, help="Number of fake samples.")
    parser.add_argument("--batch_size", type=int, default=8, help="Batch size for the fake-data smoke test.")
    parser.add_argument("--epochs", type=int, default=3, help="Number of fake-data training epochs.")
    return parser.parse_args()


__all__ = [
    "CNNGRUTerrainReconstructor",
    "run_fake_data_smoke_test",
]


if __name__ == "__main__":
    args = _parse_args()
    run_fake_data_smoke_test(
        device=args.device,
        num_samples=args.num_samples,
        batch_size=args.batch_size,
        num_epochs=args.epochs,
    )
