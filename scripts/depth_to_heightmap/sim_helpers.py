"""Helpers for the scripts that run a terrain reconstructor inside Isaac Lab. Import them after launching the app."""

from __future__ import annotations

import math
import os
import sys
from pathlib import Path

import torch
import warp as wp
from rsl_rl.runners import DistillationRunner, OnPolicyRunner

import isaaclab.sim as sim_utils
from isaaclab.markers import VisualizationMarkers, VisualizationMarkersCfg
from isaaclab.utils.assets import retrieve_file_path
from isaaclab_rl.rsl_rl import RslRlVecEnvWrapper
from isaaclab_tasks.utils import get_checkpoint_path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "l2_lidar_to_heightmap"))
import lidar_grid  # noqa: E402

# as in collect_depth_to_heightmap.py and the task's observation
HEIGHTMAP_HEIGHT_OFFSET = 0.5
DEPTH_MAX_RANGE = 2.0
# height errors (m) between the marker colours: green below the first, then 3 shades too high / too low
ERROR_THRESHOLDS = (0.01, 0.03, 0.05)
# LidarStream's extra L2 errors for the ones of the rosbag of 2026-10-30 (Go2 standing on flat ground), larger than
# unitree_l2_lidar.py's: the ground comes out up to 3 cm off, with a pattern that changes with the range (range error
# -8 cm at 0.7 m, +1 cm at 0.4 m) and with the direction (1-2 cm between neighbouring 10 cm cells), and the points of
# a 5 cm cell scatter by ~13 mm (the sensor model: 1.5-2.5 mm). collect_depth_to_heightmap.py --lidar_errors bag.
BAG_LIDAR_ERRORS = {"range_error": 0.04, "range_wavelength": (0.3, 1.2), "direction_error": 0.01,
                    "point_noise": (0.008, 0.02)}


def as_torch(value) -> torch.Tensor:
    return value.torch if hasattr(value, "torch") else value


def depth_frame(env: RslRlVecEnvWrapper) -> torch.Tensor:
    """(num_envs, 1, H, W), invalid rays = 0, clipped to the training range."""
    depth = as_torch(env.unwrapped._depth_camera.data.output["distance_to_image_plane"])
    depth = torch.nan_to_num(depth, nan=0.0, posinf=0.0, neginf=0.0).clip(0.0, DEPTH_MAX_RANGE)
    return depth.permute(0, 3, 1, 2)


def _small_rotations(num: int, max_angle: float, device) -> torch.Tensor:
    """(num, 3, 3) rotations by angles uniform in +-max_angle about x, y and z (Rodrigues)."""
    rotation_vector = (2.0 * torch.rand(num, 3, device=device) - 1.0) * max_angle
    angle = rotation_vector.norm(dim=-1, keepdim=True).unsqueeze(-1)
    k = torch.zeros(num, 3, 3, device=device)
    axis = rotation_vector / rotation_vector.norm(dim=-1, keepdim=True).clamp(min=1e-9)
    k[:, 0, 1], k[:, 0, 2], k[:, 1, 2] = -axis[:, 2], axis[:, 1], -axis[:, 0]
    k = k - k.transpose(1, 2)
    return torch.eye(3, device=device) + torch.sin(angle) * k + (1.0 - torch.cos(angle)) * k @ k


class LidarStream:
    """The L2 messages as the reconstructor gets them on the robot, put on the grid at every control step.

    The sensor (unitree_l2_lidar.py) gives the messages with the errors identified from the rosbag (scan pattern and
    timing, range noise and systematic error, missing points, motion distortion). On top of it: each message arrives
    ``latency`` (uniform range, s) after its end, and the grid uses a mount and a gravity direction slightly off, as a
    calibration and an IMU would be (``mount_position_error`` m, ``mount_angle_error`` and ``gravity_angle_error``
    rad, uniform per axis, drawn at every episode start). All zero: the exact mount and gravity, no latency.

    Optionally (``BAG_LIDAR_ERRORS``) more range errors, drawn at every episode start: ``range_error`` * sin(2 pi range /
    wavelength + phase), wavelength uniform in ``range_wavelength``; an error that changes smoothly with the direction
    of the ray, std ``direction_error``; white noise, std uniform in ``point_noise``. All in m, on the range.
    """

    DIRECTION_WAVES = 4  # the direction error: a sum of waves along random directions

    def __init__(self, env: RslRlVecEnvWrapper, latency=(0.0, 0.04), mount_position_error: float = 0.01,
                 mount_angle_error: float = math.radians(1.0), gravity_angle_error: float = math.radians(1.0),
                 range_error: float = 0.0, range_wavelength=(0.3, 1.2), direction_error: float = 0.0,
                 point_noise=(0.0, 0.0)):
        self.env, self.lidar = env.unwrapped, env.unwrapped._unitree_l2_lidar
        self.latency, self.position_error = latency, mount_position_error
        self.mount_angle_error, self.gravity_angle_error = mount_angle_error, gravity_angle_error
        self.range_error, self.range_wavelength, self.point_noise = range_error, range_wavelength, point_noise
        # a wave a sin(...) has std a / sqrt(2)
        self.direction_amplitude = direction_error / math.sqrt(self.DIRECTION_WAVES / 2)
        num, rays, device = self.env.num_envs, self.lidar.num_rays, self.env.device
        self.range_amplitude, self.range_wavenumber, self.range_phase, self.point_noise_std = torch.zeros(4, num, device=device)
        self.direction_axes = torch.zeros(num, self.DIRECTION_WAVES, 3, device=device)
        self.direction_frequency = torch.zeros(num, self.DIRECTION_WAVES, device=device)
        self.direction_phase = torch.zeros(num, self.DIRECTION_WAVES, device=device)
        self.points = torch.full((num, rays, 3), math.inf, device=device)  # latest message arrived
        self.end = torch.zeros(num, device=device)  # its end, sensor time
        self.pending = torch.full((num, rays, 3), math.inf, device=device)  # message on its way
        self.pending_end = torch.zeros(num, device=device)
        self.arrival = torch.full((num,), math.inf, device=device)
        self.rotation = lidar_grid.mount_rotation(device).repeat(num, 1, 1)
        self.position = torch.tensor(lidar_grid.MOUNT_POSITION, device=device).repeat(num, 1)
        self.gravity_rotation = torch.eye(3, device=device).repeat(num, 1, 1)
        self.last_update = self._sensor_time("_timestamp_last_update").clone()
        self.reset(torch.arange(num, device=device))

    def _sensor_time(self, name: str) -> torch.Tensor:
        return wp.to_torch(getattr(self.lidar, name)).float()

    def reset(self, env_ids: torch.Tensor) -> None:
        """New episodes: no message yet, new calibration errors."""
        num, device = len(env_ids), self.env.device
        self.points[env_ids] = math.inf
        self.arrival[env_ids] = math.inf
        self.end[env_ids] = -1.0
        self.last_update[env_ids] = self._sensor_time("_timestamp_last_update")[env_ids]
        self.rotation[env_ids] = _small_rotations(num, self.mount_angle_error, device) @ lidar_grid.mount_rotation(device)
        self.position[env_ids] = torch.tensor(lidar_grid.MOUNT_POSITION, device=device) + (
            2.0 * torch.rand(num, 3, device=device) - 1.0) * self.position_error
        self.gravity_rotation[env_ids] = _small_rotations(num, self.gravity_angle_error, device)
        uniform = lambda low, high, *shape: low + (high - low) * torch.rand(num, *shape, device=device)  # noqa: E731
        self.range_amplitude[env_ids] = uniform(0.0, self.range_error)
        self.range_wavenumber[env_ids] = 2.0 * math.pi / uniform(*self.range_wavelength)
        self.range_phase[env_ids] = uniform(0.0, 2.0 * math.pi)
        self.point_noise_std[env_ids] = uniform(*self.point_noise)
        axes = torch.randn(num, self.DIRECTION_WAVES, 3, device=device)
        self.direction_axes[env_ids] = axes / axes.norm(dim=-1, keepdim=True)
        # 3-20 rad per unit of cosine: features of ~20-120 deg, 10-60 cm on the ground at 0.5 m
        self.direction_frequency[env_ids] = uniform(3.0, 20.0, self.DIRECTION_WAVES)
        self.direction_phase[env_ids] = uniform(0.0, 2.0 * math.pi, self.DIRECTION_WAVES)

    def _range_errors(self, points: torch.Tensor, envs: torch.Tensor) -> torch.Tensor:
        """The extra range errors on the points (L2 frame) of a message of the envs ``envs`` (mask)."""
        ranges = points.norm(dim=-1, keepdim=True)
        directions = points / ranges
        error = self.range_amplitude[envs, None, None] * torch.sin(
            self.range_wavenumber[envs, None, None] * ranges + self.range_phase[envs, None, None])
        waves = torch.sin(self.direction_frequency[envs, None] * (directions @ self.direction_axes[envs].transpose(1, 2))
                          + self.direction_phase[envs, None])
        error = error + self.direction_amplitude * waves.sum(dim=-1, keepdim=True)
        error = error + self.point_noise_std[envs, None, None] * torch.randn_like(ranges)
        return points * (1.0 + error / ranges)  # missing points (inf) stay not finite

    def grid(self, dones: torch.Tensor) -> torch.Tensor:
        """The grid now, (num_envs, channels, rows, cols); ``dones`` are the envs reset at this step."""
        dones = dones.bool()
        if dones.any():
            self.reset(dones.nonzero().flatten())
        now, last_update = self._sensor_time("_timestamp"), self._sensor_time("_timestamp_last_update")
        new = (last_update != self.last_update) & ~dones
        self.last_update = last_update.clone()
        if new.any():
            latency = self.latency[0] + (self.latency[1] - self.latency[0]) * torch.rand(int(new.sum()), device=now.device)
            self.pending[new] = self._range_errors(self.lidar.points_l2[new], new)
            self.pending_end[new] = last_update[new]
            self.arrival[new] = last_update[new] + latency
        arrived = self.arrival <= now + 1e-6
        if arrived.any():
            self.points[arrived] = self.pending[arrived]
            self.end[arrived] = self.pending_end[arrived]
            self.arrival[arrived] = math.inf
        gravity = (self.gravity_rotation @ as_torch(self.env._robot.data.projected_gravity_b).unsqueeze(-1)).squeeze(-1)
        age = torch.where(self.end >= 0.0, now - self.end, 1.0)
        return lidar_grid.lidar_grid(self.points, gravity, age, self.rotation, self.position)


class SensorFrames:
    """The reconstructor's sensor input at every control step: the depth frame, or the grid of the latest LiDAR message
    (``LidarStream``, with its latency and calibration errors). Call it at every step with the envs reset at that step."""

    def __init__(self, env: RslRlVecEnvWrapper, model_config: dict):
        self.env = env
        lidar = model_config.get("sensor", "depth") == "lidar"
        self.lidar = LidarStream(env, **model_config.get("lidar_errors", {})) if lidar else None

    def __call__(self, dones: torch.Tensor) -> torch.Tensor:
        return depth_frame(self.env) if self.lidar is None else self.lidar.grid(dones)


def true_heightmap(env: RslRlVecEnvWrapper) -> torch.Tensor:
    """(num_envs, cells): the heightmap the task puts in the policy observation, before observation noise."""
    scanner = env.unwrapped._perceptive_height_scanner
    heights = as_torch(scanner.data.pos_w)[:, 2:3] - as_torch(scanner.data.ray_hits_w)[..., 2] - HEIGHTMAP_HEIGHT_OFFSET
    return torch.nan_to_num(heights, nan=0.0, posinf=1.0, neginf=-1.0).clip(-1.0, 1.0)


def heightmap_slice(obs, env: RslRlVecEnvWrapper) -> slice:
    """Where the heightmap sits in the policy observation ('common' observation, then the heightmap), checked."""
    common_dim, cells = obs["common"].shape[1], true_heightmap(env).shape[1]
    where = slice(common_dim, common_dim + cells)
    if not torch.allclose(obs["policy"][:, :common_dim], obs["common"]) or not torch.allclose(
        obs["policy"][:, where], true_heightmap(env)
    ):
        raise RuntimeError("The policy observation is not ['common', heightmap]: cannot replace the heightmap.")
    return where


def configure_from_checkpoint(env_cfg, model_metadata: dict) -> None:
    """Sensor (depth camera or LiDAR) and velocity commands as in the reconstructor's training data."""
    env_cfg.forward_commands = model_metadata.get("commands") == "forward"
    lidar = model_metadata.get("sensor", "depth") == "lidar"
    env_cfg.use_unitree_l2_lidar, env_cfg.use_depth_camera = lidar, not lidar
    if lidar:
        return
    camera_cfg = env_cfg.depth_camera
    if "camera_offset_rot_xyzw" in model_metadata:
        camera_cfg.offset.pos = tuple(model_metadata["camera_offset_pos"])
        camera_cfg.offset.rot = tuple(model_metadata["camera_offset_rot_xyzw"])
        camera_cfg.offset.convention = model_metadata.get("camera_offset_convention", camera_cfg.offset.convention)
    if "camera_horizontal_aperture" in model_metadata:
        camera_cfg.pattern_cfg.focal_length = model_metadata["camera_focal_length"]
        camera_cfg.pattern_cfg.horizontal_aperture = model_metadata["camera_horizontal_aperture"]
    if "depth_image_size" in model_metadata:
        camera_cfg.pattern_cfg.height, camera_cfg.pattern_cfg.width = model_metadata["depth_image_size"]


def policy_checkpoint_path(args_cli, agent_cfg, model_metadata: dict) -> str:
    """--checkpoint, else the policy that recorded the reconstructor's data, else the latest run."""
    if getattr(args_cli, "checkpoint", None):
        return retrieve_file_path(args_cli.checkpoint)
    if Path(str(model_metadata.get("checkpoint_path", ""))).is_file():
        return str(model_metadata["checkpoint_path"])
    log_root_path = os.path.abspath(os.path.join("logs", "rsl_rl", agent_cfg.experiment_name))
    return get_checkpoint_path(log_root_path, agent_cfg.load_run, agent_cfg.load_checkpoint)


def load_policy(env: RslRlVecEnvWrapper, agent_cfg, checkpoint: str):
    runner_class = {"OnPolicyRunner": OnPolicyRunner, "DistillationRunner": DistillationRunner}[agent_cfg.class_name]
    runner = runner_class(env, agent_cfg.to_dict(), log_dir=None, device=agent_cfg.device)
    runner.load(checkpoint)
    return runner.get_inference_policy(device=env.unwrapped.device)


def marker_legend(mode: str = "tiles", show_ground_truth: bool = False, thresholds=ERROR_THRESHOLDS) -> str:
    t1, t2, t3 = (round(threshold * 100) for threshold in thresholds)
    legend = {
        "tiles": f"tiles = predicted heightmap, coloured by error: green <{t1} cm | ground too high: yellow {t1}-{t2}, "
        f"orange {t2}-{t3}, red >{t3} | too low: cyan, blue, purple",
        "spheres": "blue spheres = predicted ground height (the error is their distance from the terrain)",
        "hidden": "heightmap not drawn",
    }[mode]
    return legend + (" | white dots = true ground" if show_ground_truth and mode != "hidden" else "")


class HeightmapSurface:
    """The predicted heightmap of one env, drawn in one of ``MODES`` (``mode`` can change at any time):

    - "tiles": a tile per cell at its predicted ground height, turned with the robot's heading and coloured by the error
      against the height scanner at that cell: green close; yellow / orange / red = ground drawn too high (a drop is
      missed); cyan / blue / purple = drawn too low (thresholds ``ERROR_THRESHOLDS``). The tiles float 1 cm above their
      height, so that a correct one does not flicker in the terrain.
    - "spheres": the prediction alone, a blue sphere per cell resting on its predicted ground height.
    - "hidden": nothing drawn.

    With ``show_ground_truth``, small white dots mark the true ground: hidden under a correct tile or sphere, visible
    next to a wrong one.
    """

    MODES = ("tiles", "spheres", "hidden")
    # 0 close, 1-3 too high, 4-6 too low (growing error)
    ERROR_COLORS = ((0.1, 0.9, 0.1), (1.0, 0.9, 0.1), (1.0, 0.5, 0.05), (0.9, 0.05, 0.05),
                    (0.2, 0.9, 1.0), (0.1, 0.35, 1.0), (0.5, 0.1, 0.8))
    SPHERE_COLOR = (0.15, 0.45, 1.0)

    def __init__(self, cell_size: float = 0.1, show_ground_truth: bool = False, mode: str = "tiles",
                 sphere_radius: float = 0.02, thresholds=ERROR_THRESHOLDS):
        self.thresholds, self.thickness, self.lift, self.radius, self.mode = thresholds, 0.01, 0.01, sphere_radius, mode

        def markers(path: str, shapes: dict) -> VisualizationMarkers:
            return VisualizationMarkers(VisualizationMarkersCfg(prim_path=path, markers=shapes))

        def material(color: tuple[float, float, float]) -> sim_utils.PreviewSurfaceCfg:
            return sim_utils.PreviewSurfaceCfg(diffuse_color=color)

        tile = (0.9 * cell_size, 0.9 * cell_size, self.thickness)
        self.tiles = markers("/Visuals/DepthHeightmapSurface", {
            f"error_{i}": sim_utils.CuboidCfg(size=tile, visual_material=material(color))
            for i, color in enumerate(self.ERROR_COLORS)
        })
        self.spheres = markers("/Visuals/DepthHeightmapPrediction", {
            "prediction": sim_utils.SphereCfg(radius=sphere_radius, visual_material=material(self.SPHERE_COLOR))
        })
        self.truth = None
        if show_ground_truth:
            self.truth = markers("/Visuals/DepthHeightmapTarget", {
                "target": sim_utils.SphereCfg(radius=0.009, visual_material=material((1.0, 1.0, 1.0)))
            })
        self.set_visibility(True)

    def set_visibility(self, visible: bool) -> None:
        self.visible, self.shown_mode = visible, self.mode
        self.tiles.set_visibility(visible and self.mode == "tiles")
        self.spheres.set_visibility(visible and self.mode == "spheres")
        if self.truth is not None:
            self.truth.set_visibility(visible and self.mode != "hidden")

    def next_mode(self) -> None:
        """Switch to the next way of drawing; applied at the next update (safe from a keyboard callback)."""
        self.mode = self.MODES[(self.MODES.index(self.mode) + 1) % len(self.MODES)]

    def update(self, env: RslRlVecEnvWrapper, env_id: int, predicted: torch.Tensor) -> torch.Tensor:
        """Draw one env's predicted heightmap (metres, the task's convention, any shape with the cells in ray order),
        showing it if hidden; returns the predicted minus true ground height of each cell (> 0: ground drawn too high),
        shaped as predicted."""
        if not self.visible or self.shown_mode != self.mode:
            self.set_visibility(True)  # hidden markers ignore visualize()
        scanner = env.unwrapped._perceptive_height_scanner
        sensor_z = as_torch(scanner.data.pos_w)[env_id, 2]
        ray_hits = as_torch(scanner.data.ray_hits_w)[env_id]
        # the heightmap stores sensor height - ground height - offset, with the scanner rays in the same order
        predicted_z = sensor_z - predicted.reshape(-1) - HEIGHTMAP_HEIGHT_OFFSET
        error = predicted_z - ray_hits[:, 2]
        valid = torch.isfinite(predicted_z) & torch.isfinite(ray_hits).all(dim=1)

        if self.mode == "tiles":
            level = sum((error.abs() >= threshold).long() for threshold in self.thresholds)  # 0 .. 3
            indices = torch.where(error >= 0, level, torch.where(level > 0, level + 3, 0))
            centers = torch.cat((ray_hits[:, :2], (predicted_z + self.lift + 0.5 * self.thickness).unsqueeze(1)), dim=1)
            # the grid turns with the robot's heading only (yaw-aligned scanner); quaternions are (x, y, z, w)
            x, y, z, w = as_torch(scanner.data.quat_w)[env_id].unbind(-1)
            yaw = torch.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))
            heading = torch.stack((torch.zeros_like(yaw), torch.zeros_like(yaw), torch.sin(yaw / 2), torch.cos(yaw / 2)))
            self.tiles.visualize(
                translations=centers[valid], orientations=heading.expand(int(valid.sum()), 4), marker_indices=indices[valid]
            )
        elif self.mode == "spheres":
            # spheres resting on the predicted surface, not half buried in it
            centers = torch.cat((ray_hits[:, :2], (predicted_z + self.radius).unsqueeze(1)), dim=1)
            self.spheres.visualize(translations=centers[valid])
        if self.truth is not None and self.mode != "hidden":
            self.truth.visualize(translations=ray_hits[valid] + torch.tensor([0.0, 0.0, 0.009], device=ray_hits.device))
        return error.view_as(predicted)
