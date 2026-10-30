"""Helpers for the scripts that run a terrain reconstructor inside Isaac Lab. Import them after launching the app."""

from __future__ import annotations

import os
from pathlib import Path

import torch
from rsl_rl.runners import DistillationRunner, OnPolicyRunner

import isaaclab.sim as sim_utils
from isaaclab.markers import VisualizationMarkers, VisualizationMarkersCfg
from isaaclab.utils.assets import retrieve_file_path
from isaaclab_rl.rsl_rl import RslRlVecEnvWrapper
from isaaclab_tasks.utils import get_checkpoint_path

# as in collect_depth_to_heightmap.py and the task's observation
HEIGHTMAP_HEIGHT_OFFSET = 0.5
DEPTH_MAX_RANGE = 2.0
# height errors (m) between the marker colours: green below the first, then 3 shades too high / too low
ERROR_THRESHOLDS = (0.01, 0.03, 0.05)


def as_torch(value) -> torch.Tensor:
    return value.torch if hasattr(value, "torch") else value


def depth_frame(env: RslRlVecEnvWrapper) -> torch.Tensor:
    """(num_envs, 1, H, W), invalid rays = 0, clipped to the training range."""
    depth = as_torch(env.unwrapped._depth_camera.data.output["distance_to_image_plane"])
    depth = torch.nan_to_num(depth, nan=0.0, posinf=0.0, neginf=0.0).clip(0.0, DEPTH_MAX_RANGE)
    return depth.permute(0, 3, 1, 2)


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
    """Depth camera and velocity commands as in the reconstructor's training data."""
    env_cfg.use_depth_camera = True
    env_cfg.forward_commands = model_metadata.get("commands") == "forward"
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
