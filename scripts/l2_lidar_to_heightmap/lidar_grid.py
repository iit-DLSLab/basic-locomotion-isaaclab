"""Unitree L2 point cloud -> grid around the robot: the LiDAR input of the terrain reconstructor.

Plain torch, the same code in simulation and on the robot. Input: the points of the latest /utlidar/cloud message (L2
frame, as published), the gravity direction in the base frame (IMU) and the age of the message at the current
control step. The points go to the base frame with the L2 mount, then to the yaw-aligned base frame of the policy
heightmap with the gravity, and fall into 5 cm cells. Heights use the heightmap convention (base z - ground z - 0.5).

The grid has the layout of the policy heightmap: rows along y (right -> left), columns along x (back -> front). Its
cells are a quarter of the heightmap's 10 cm cells, so a stride-2 conv of the reconstructor gives 10 cm cells
centred on the heightmap cells (``heightmap_crop``).
"""

from __future__ import annotations

import math

import torch
from torch import Tensor

# The L2 on the Go2 (L2 frame -> base frame, quaternion xyzw), as unitree_l2_lidar in go2_env_cfg.py. Calibrated on the
# rosbag of 2026-10-30 (robot standing on flat ground): the ground plane of the cloud against the IMU gravity and the
# feet from the joint angles. The L2 z axis points down, 13.2 deg forward (the Unitree URDF says 15); its x axis points
# forward-right, at -59 deg from the base x: the URDF / feat/new_start_stop rotation (x backward) tilts the real ground
# by several cm. The height is the effective one (it takes in the mean range error at 0.3-0.6 m); x and y are the
# URDF's radar joint. Recheck on the robot with calibrate_mount.py when the sensor or its mount change.
MOUNT_POSITION = (0.28945, 0.0, 0.0507)
MOUNT_QUAT_XYZW = (-0.86610, 0.48649, -0.10267, 0.05160)

RESOLUTION = 0.05
X_RANGE = (-0.15, 0.95)  # around the heightmap (x 0.1-0.7 m), with room for the motion between messages
Y_RANGE = (-0.65, 0.65)  # heightmap y -0.4-0.4 m
HEIGHT_OFFSET = 0.5  # heights = base z - ground z - HEIGHT_OFFSET, clipped to [-1, 1], as in the policy heightmap
CHANNELS = ("mean height", "min height", "max height", "points", "age")
COUNT_SCALE = math.log1p(64.0)  # log(1 + points) / COUNT_SCALE
AGE_SCALE = 0.1  # s


def grid_shape() -> tuple[int, int]:
    """(rows, cols) of the grid: y cells, x cells."""
    return round((Y_RANGE[1] - Y_RANGE[0]) / RESOLUTION), round((X_RANGE[1] - X_RANGE[0]) / RESOLUTION)


def heightmap_crop(heightmap_x0: float, heightmap_y0: float) -> tuple[int, int]:
    """(row, col) of the first heightmap cell (centre heightmap_x0, heightmap_y0) among the 10 cm cells made of 2 x 2
    grid cells, centred at Y_RANGE[0] + (2 i + 1) RESOLUTION and X_RANGE[0] + (2 j + 1) RESOLUTION."""
    row = (heightmap_y0 - Y_RANGE[0] - RESOLUTION) / (2 * RESOLUTION)
    col = (heightmap_x0 - X_RANGE[0] - RESOLUTION) / (2 * RESOLUTION)
    if abs(row - round(row)) > 1e-6 or abs(col - round(col)) > 1e-6:
        raise ValueError(f"The heightmap cells ({heightmap_x0}, {heightmap_y0}) do not fall on the grid's 10 cm cells.")
    return round(row), round(col)


def mount_rotation(device: str | torch.device | None = None) -> Tensor:
    """(3, 3) rotation from the L2 frame to the base frame."""
    return rotation_matrix(MOUNT_QUAT_XYZW, device)


def rotation_matrix(quat_xyzw, device: str | torch.device | None = None) -> Tensor:
    """(3, 3) rotation matrix of a unit quaternion (x, y, z, w)."""
    x, y, z, w = quat_xyzw
    return torch.tensor(
        (
            (1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)),
            (2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)),
            (2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)),
        ),
        device=device,
    )


def lidar_grid(
    points_l2: Tensor,
    projected_gravity: Tensor,
    age: Tensor,
    rotation: Tensor | None = None,
    position: Tensor | None = None,
    range_error: tuple[Tensor, Tensor] | None = None,
) -> Tensor:
    """The grid of N robots.

    Args:
        points_l2: (N, R, 3) points of the latest message in the L2 frame; slots without a point are not finite.
        projected_gravity: (N, 3) gravity direction in the base frame (the policy's projected gravity).
        age: (N,) time from the end of the message to now, in s.
        rotation, position: L2 frame -> base frame, (3, 3) and (3,) or per robot (N, 3, 3) and (N, 3); the mount by
            default.
        range_error: on the robot, the L2's range error (measured - true) at some ranges, (K,) and (K,), increasing
            ranges (calibrate_mount.py); taken off the points, constant beyond the first and last range.

    Returns:
        (N, len(CHANNELS), rows, cols): per cell the mean, min and max height of its points (0 without points), the
        number of points (log scale) and the age of the message (the same in every cell).
    """
    num_robots, device = points_l2.shape[0], points_l2.device
    rows, cols = grid_shape()
    if rotation is None:
        rotation = mount_rotation(device)
    if position is None:
        position = torch.tensor(MOUNT_POSITION, device=device)
    valid = torch.isfinite(points_l2).all(dim=-1)
    points = torch.where(valid.unsqueeze(-1), points_l2, 0.0)
    if range_error is not None:
        knots, error = range_error
        ranges = points.norm(dim=-1, keepdim=True).clamp(min=1e-6)
        clamped = ranges.clamp(knots[0], knots[-1])
        upper = torch.searchsorted(knots, clamped.contiguous()).clamp(1, len(knots) - 1)
        weight = (clamped - knots[upper - 1]) / (knots[upper] - knots[upper - 1])
        points = points * (1.0 - (error[upper - 1] + weight * (error[upper] - error[upper - 1])) / ranges)
    points_base = points @ rotation.transpose(-1, -2) + position.view(-1, 1, 3)

    # yaw-aligned frame: z up (against gravity), x the base's x on the horizontal plane
    up = -projected_gravity / projected_gravity.norm(dim=-1, keepdim=True)
    forward = torch.zeros_like(up)
    forward[:, 0] = 1.0
    forward = forward - up[:, :1] * up
    forward = forward / forward.norm(dim=-1, keepdim=True)
    left = torch.cross(up, forward, dim=-1)
    points_yaw = points_base @ torch.stack((forward, left, up), dim=1).transpose(1, 2)

    height = (-points_yaw[..., 2] - HEIGHT_OFFSET).clip(-1.0, 1.0)
    col = torch.floor((points_yaw[..., 0] - X_RANGE[0]) / RESOLUTION).long()
    row = torch.floor((points_yaw[..., 1] - Y_RANGE[0]) / RESOLUTION).long()
    inside = valid & (col >= 0) & (col < cols) & (row >= 0) & (row < rows)
    cells = rows * cols
    robot = torch.arange(num_robots, device=device).view(-1, 1)
    # points outside the grid go to an extra cell, dropped at the end
    index = torch.where(inside, robot * cells + row * cols + col, num_robots * cells).flatten()
    height = height.flatten()

    size = num_robots * cells + 1
    count = torch.zeros(size, device=device).index_add_(0, index, torch.ones_like(height))
    total = torch.zeros(size, device=device).index_add_(0, index, height)
    lowest = torch.full((size,), math.inf, device=device).scatter_reduce_(0, index, height, "amin")
    highest = torch.full((size,), -math.inf, device=device).scatter_reduce_(0, index, height, "amax")
    count, total, lowest, highest = (value[:-1].view(num_robots, rows, cols) for value in (count, total, lowest, highest))
    hit = count > 0
    channels = (
        torch.where(hit, total / count.clamp(min=1.0), 0.0),
        torch.where(hit, lowest, 0.0),
        torch.where(hit, highest, 0.0),
        torch.log1p(count) / COUNT_SCALE,
        (age / AGE_SCALE).view(-1, 1, 1).expand(num_robots, rows, cols),
    )
    return torch.stack(channels, dim=1)
