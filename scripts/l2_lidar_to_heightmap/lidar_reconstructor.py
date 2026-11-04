"""The LiDAR terrain reconstructor on the robot: plain torch, one call per policy step.

Export a trained checkpoint (terrain_reconstruction_mlp.py, collector --sensor lidar) to TorchScript:

    python scripts/l2_lidar_to_heightmap/lidar_reconstructor.py --checkpoint <model>.pt --output <model>.ts

On the robot it needs only torch, lidar_grid.py, this file and the .ts file:

    reconstructor = LidarTerrainReconstructor("<model>.ts")
    # every /utlidar/cloud message (x, y, z of its points, in the L2 frame as published), with its header stamp
    reconstructor.lidar_message(points_xyz, stamp)
    # every policy step: the policy observation without the heightmap (the task's 'common' observation, the stack of
    # the last 5 steps, oldest first), the projected gravity of the observation, the time (same clock as the stamps)
    heights = reconstructor.step(common_obs, projected_gravity, now)

``heights`` is the heightmap of the policy observation: (cells,) in the order of the task's height scanner, base z -
ground z - 0.5, clipped to [-1, 1]. ``reset()`` when the controller (re)starts: the first step gives flat ground and the
memory starts from the next one, as in training.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import torch

import lidar_grid

# the L2 publishes a message after 64.9 ms of scan, stamped with the time of its first point (unitree_l2_lidar.py)
MESSAGE_PERIOD = 0.0649


class LidarTerrainReconstructor:
    def __init__(self, path: str | Path, device: str = "cpu", calibration: str | Path | None = None):
        extra_files = {"config.json": ""}
        self.model = torch.jit.load(str(path), map_location=device, _extra_files=extra_files)
        self.config = json.loads(extra_files["config.json"])
        self.device = device
        self.message_period = MESSAGE_PERIOD
        # the robot's L2 (calibrate_mount.py --output): its mount and range error, else lidar_grid.py's mount
        self.rotation = self.position = self.range_error = None
        if calibration is not None:
            with open(calibration) as file:
                values = json.load(file)
            self.rotation = lidar_grid.rotation_matrix(values["mount_quat_xyzw"], device)
            self.position = torch.tensor(values["mount_position"], device=device)
            self.range_error = (torch.tensor(values["range_knots"], device=device),
                                torch.tensor(values["range_error"], device=device))
        self.reset()

    def reset(self) -> None:
        self.hidden = torch.zeros(1, 1, self.config["hidden_dim"], device=self.device)
        self.points = torch.full((1, 1, 3), math.inf, device=self.device)
        self.message_end = None
        self.fresh = True

    def lidar_message(self, points_xyz, stamp: float) -> None:
        self.points = torch.as_tensor(points_xyz, dtype=torch.float32, device=self.device).reshape(1, -1, 3)
        self.message_end = stamp + MESSAGE_PERIOD

    @torch.no_grad()
    def step(self, common_obs, projected_gravity, now: float) -> torch.Tensor:
        age = now - self.message_end if self.message_end is not None else 1.0
        grid = lidar_grid.lidar_grid(
            self.points,
            torch.as_tensor(projected_gravity, dtype=torch.float32, device=self.device).reshape(1, 3),
            torch.tensor([age], dtype=torch.float32, device=self.device),
            self.rotation,
            self.position,
            self.range_error,
        )
        common_obs = torch.as_tensor(common_obs, dtype=torch.float32, device=self.device).reshape(1, -1)
        heights, hidden = self.model(grid, common_obs, self.hidden)
        if self.fresh:
            self.fresh = False
            return torch.full_like(heights, self.config["flat_height"])
        self.hidden = hidden
        return heights


class _Step(torch.nn.Module):
    """One step of a trained reconstructor with plain tensors in and out, for TorchScript."""

    def __init__(self, model: torch.nn.Module, mean: float, std: float):
        super().__init__()
        self.model, self.mean, self.std = model, mean, std

    def forward(self, grid: torch.Tensor, common_obs: torch.Tensor, hidden: torch.Tensor):
        output = self.model(depth_data=grid[:, None], robot_info=common_obs[:, None], hidden_state=hidden)
        heights = (output.refined_heightmap.reshape(-1) * self.std + self.mean).clamp(-1.0, 1.0)
        return heights, output.hidden_state


def export(checkpoint_path: str, output_path: str) -> None:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "depth_to_heightmap"))
    from terrain_reconstruction_mlp import build_terrain_reconstructor

    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
    model_config = checkpoint["model_config"]
    if model_config.get("sensor") != "lidar":
        raise ValueError(f"{checkpoint_path} is not a LiDAR reconstructor.")
    model = build_terrain_reconstructor(model_config)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()
    normalization = checkpoint["target_normalization"]
    step = _Step(model, normalization["mean"], normalization["std"]).eval()
    hidden_dim = model.memory.hidden_size
    example = (
        torch.zeros(1, len(lidar_grid.CHANNELS), *lidar_grid.grid_shape()),
        torch.zeros(1, model_config["proprio_dim"]),
        torch.zeros(1, 1, hidden_dim),
    )
    with torch.no_grad():
        traced = torch.jit.trace(step, example, check_trace=False)
        # the traced step must match the model on a random input
        inputs = (torch.randn_like(example[0]), torch.randn_like(example[1]), torch.randn_like(example[2]))
        difference = (traced(*inputs)[0] - step(*inputs)[0]).abs().max().item()
    config = {
        "hidden_dim": hidden_dim,
        "proprio_dim": model_config["proprio_dim"],
        "heightmap_size": list(model_config["heightmap_size"]),
        "flat_height": normalization["mean"],
        "grid": {"resolution": lidar_grid.RESOLUTION, "x_range": lidar_grid.X_RANGE, "y_range": lidar_grid.Y_RANGE,
                 "channels": list(lidar_grid.CHANNELS)},
        "mount_position": lidar_grid.MOUNT_POSITION,
        "mount_quat_xyzw": lidar_grid.MOUNT_QUAT_XYZW,
        "checkpoint": str(Path(checkpoint_path).resolve()),
    }
    if checkpoint.get("dataset_metadata", {}).get("lidar_grid", {}).get("shape") not in (None, lidar_grid.grid_shape()):
        raise ValueError("The checkpoint was trained on another grid than lidar_grid.py's.")
    torch.jit.save(traced, output_path, _extra_files={"config.json": json.dumps(config)})
    print(f"[INFO] Exported {checkpoint_path} to {output_path} (max difference to the model {difference:.1e})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export a LiDAR terrain reconstructor to TorchScript for the robot.")
    parser.add_argument("--checkpoint", required=True, help="Checkpoint of terrain_reconstruction_mlp.py.")
    parser.add_argument("--output", required=True, help="TorchScript file to write.")
    args = parser.parse_args()
    export(args.checkpoint, args.output)
