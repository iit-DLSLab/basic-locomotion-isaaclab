# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Collect a depth-to-heightmap dataset using a trained locomotion policy."""

"""Launch Isaac Sim Simulator first."""

import argparse
import os
import sys
from collections import deque

from isaaclab.app import AppLauncher

# local imports
import cli_args  # isort: skip

# add argparse arguments
parser = argparse.ArgumentParser(description="Collect a terrain reconstruction dataset with a trained RSL-RL policy.")
parser.add_argument("--video", action="store_true", default=False, help="Record videos during collection.")
parser.add_argument("--video_length", type=int, default=200, help="Length of the recorded video (in steps).")
parser.add_argument(
    "--disable_fabric", action="store_true", default=False, help="Disable fabric and use USD I/O operations."
)
parser.add_argument("--num_envs", type=int, default=None, help="Number of environments to simulate.")
parser.add_argument("--task", type=str, default=None, help="Name of the task.")
parser.add_argument(
    "--agent", type=str, default="rsl_rl_cfg_entry_point", help="Name of the RL agent configuration entry point."
)
parser.add_argument("--seed", type=int, default=None, help="Seed used for the environment.")
parser.add_argument(
    "--use_pretrained_checkpoint",
    action="store_true",
    help="Use the pre-trained checkpoint from Nucleus.",
)
parser.add_argument("--real-time", action="store_true", default=False, help="Run in real-time, if possible.")
parser.add_argument(
    "--dataset_path",
    type=str,
    default=None,
    help="Where to save the collected dataset. Defaults to <checkpoint_dir>/terrain_reconstruction_dataset.pt.",
)
parser.add_argument(
    "--num_collection_rollouts",
    type=int,
    default=25,
    help="Number of rollout windows to collect before saving the dataset.",
)
parser.add_argument(
    "--rollout_horizon",
    type=int,
    default=None,
    help="Optional fixed rollout length. Defaults to the environment max episode length when available.",
)
parser.add_argument(
    "--depth_history_length",
    type=int,
    default=5,
    help="Number of depth frames per saved training sample.",
)
parser.add_argument(
    "--depth_history_stride",
    type=int,
    default=1,
    help=(
        "Simulation steps between consecutive saved depth frames. With stride S and length L, a sample covers the"
        " last (L - 1) * S steps (always including the newest frame) at the cost of L frames."
    ),
)
parser.add_argument(
    "--proprio_history_length",
    type=int,
    default=50,
    help="Number of robot-info frames per saved training sample.",
)
parser.add_argument(
    "--max_dataset_samples",
    type=int,
    default=10000,
    help="Maximum number of training samples to keep in the saved dataset.",
)
parser.add_argument(
    "--samples_per_step",
    type=int,
    default=None,
    help=(
        "Maximum number of randomly chosen environments added to the dataset per simulation step. Spreads the"
        " sample budget over whole episodes instead of filling it within a few steps. Defaults to all valid ones."
    ),
)
parser.add_argument(
    "--depth_dtype",
    type=str,
    choices=("float16", "float32"),
    default="float16",
    help="Storage dtype for depth frames. float16 halves the dataset memory (~1 mm precision in the 0-2 m range).",
)
parser.add_argument(
    "--save_every_rollouts",
    type=int,
    default=5,
    help="Save an intermediate dataset checkpoint every N rollout windows.",
)
parser.add_argument(
    "--shifted_heightmap_center_x",
    type=float,
    default=None,
    help=(
        "Also save 'heightmaps_shifted': the policy's heightmap grid with its centre moved to this x in the base frame"
        " [m], ray-cast by a separate target-only scanner. The policy keeps reading its own heightmap."
    ),
)
# append RSL-RL cli arguments
cli_args.add_rsl_rl_args(parser)
# append AppLauncher cli args
AppLauncher.add_app_launcher_args(parser)
# parse the arguments
args_cli, hydra_args = parser.parse_known_args()
# always enable cameras to record video
if args_cli.video:
    args_cli.enable_cameras = True

# clear out sys.argv for Hydra
sys.argv = [sys.argv[0]] + hydra_args

# launch omniverse app
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

"""Rest everything follows."""

import importlib.metadata as importlib_metadata

import gymnasium as gym
import torch

from rsl_rl.runners import DistillationRunner, OnPolicyRunner

from isaaclab.envs import (
    DirectMARLEnv,
    DirectMARLEnvCfg,
    DirectRLEnvCfg,
    ManagerBasedRLEnvCfg,
    multi_agent_to_single_agent,
)
from isaaclab.utils.assets import retrieve_file_path
from isaaclab.utils.dict import print_dict
from isaaclab_rl.utils.pretrained_checkpoint import get_published_pretrained_checkpoint

from isaaclab_rl.rsl_rl import RslRlBaseRunnerCfg, RslRlVecEnvWrapper, handle_deprecated_rsl_rl_cfg

import isaaclab_tasks  # noqa: F401
import basic_locomotion_isaaclab.tasks  # noqa: F401

from isaaclab_tasks.utils import get_checkpoint_path
from isaaclab_tasks.utils.hydra import hydra_task_config


class TerrainReconstructionDatasetBuilder:
    def __init__(self, max_samples: int, depth_dtype: torch.dtype = torch.float32):
        self.max_samples = max_samples
        self.depth_dtype = depth_dtype
        self.batches: dict[str, list[torch.Tensor]] = {}
        self.num_samples = 0

    def add_batch(self, **tensors: torch.Tensor) -> int:
        """Add per-sample tensors (same leading batch size); ``depth_data`` is stored with ``depth_dtype``."""
        if self.num_samples >= self.max_samples:
            return 0

        remaining = self.max_samples - self.num_samples
        batch_size = next(iter(tensors.values())).shape[0]
        if batch_size > remaining:
            selected_indices = torch.randperm(batch_size, device=tensors["depth_data"].device)[:remaining]
            tensors = {name: tensor[selected_indices] for name, tensor in tensors.items()}
            batch_size = remaining

        for name, tensor in tensors.items():
            tensor = tensor.detach().to(self.depth_dtype) if name == "depth_data" else tensor.detach()
            self.batches.setdefault(name, []).append(tensor.cpu())
        self.num_samples += batch_size
        return batch_size

    def save(self, dataset_path: str, metadata: dict) -> None:
        if self.num_samples == 0:
            raise RuntimeError("No dataset samples were collected, so nothing can be saved.")

        dataset_dir = os.path.dirname(dataset_path)
        if dataset_dir:
            os.makedirs(dataset_dir, exist_ok=True)
        # merge one key at a time and keep only the merged tensor, so the peak is one extra copy of the largest key
        for name, batches in self.batches.items():
            self.batches[name] = [torch.cat(batches, dim=0)]
        dataset = {
            **{name: batches[0] for name, batches in self.batches.items()},
            "metadata": {
                **metadata,
                "num_samples": self.num_samples,
            },
        }
        torch.save(dataset, dataset_path)
        print(f"[INFO] Saved terrain reconstruction dataset to: {dataset_path}")


# heightmap values are (sensor origin z - terrain z - HEIGHTMAP_HEIGHT_OFFSET), as in the policy observation
HEIGHTMAP_HEIGHT_OFFSET = 0.5
DEPTH_MAX_RANGE = 2.0


def _as_torch(value) -> torch.Tensor:
    return value.torch if hasattr(value, "torch") else value


def _sanitize_depth_data(env: RslRlVecEnvWrapper) -> torch.Tensor:
    depth_data = env.unwrapped._depth_camera.data.output["distance_to_image_plane"]
    # rays that hit nothing are invalid (0), like the holes of a real depth sensor
    depth_data = torch.nan_to_num(depth_data, nan=0.0, posinf=0.0, neginf=0.0)
    depth_data = depth_data.clip(0.0, DEPTH_MAX_RANGE)
    depth_data = depth_data.permute(0, 3, 1, 2)
    return depth_data


def _matrix_from_quat_xyzw(quat: torch.Tensor) -> torch.Tensor:
    x, y, z, w = quat.unbind(-1)
    matrix = torch.stack(
        (
            1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w),
            2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w),
            2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y),
        ),
        dim=-1,
    )
    return matrix.view(*quat.shape[:-1], 3, 3)


def _get_camera_poses(env: RslRlVecEnvWrapper) -> tuple[torch.Tensor, torch.Tensor]:
    """World position and rotation of the depth camera frame (x forward along the optical axis, y left, z up)."""
    camera_data = env.unwrapped._depth_camera.data
    return _as_torch(camera_data.pos_w).clone(), _matrix_from_quat_xyzw(_as_torch(camera_data.quat_w_world))


def _camera_poses_in_heightmap_frame(
    camera_positions: torch.Tensor, camera_rotations: torch.Tensor, scanner, env_ids: torch.Tensor
) -> tuple[torch.Tensor, torch.Tensor]:
    """Express camera poses (B, T, 3) / (B, T, 3, 3) in the current yaw-aligned heightmap frame of ``scanner``.

    In that frame, a terrain point p has heightmap value ``-p_z - HEIGHTMAP_HEIGHT_OFFSET`` at the cell under it.
    """
    origin = _as_torch(scanner.data.pos_w)[env_ids]
    x, y, z, w = _as_torch(scanner.data.quat_w)[env_ids].unbind(-1)
    yaw = torch.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))
    cos_yaw, sin_yaw, zeros, ones = yaw.cos(), yaw.sin(), torch.zeros_like(yaw), torch.ones_like(yaw)
    world_to_heightmap = torch.stack(
        (cos_yaw, sin_yaw, zeros, -sin_yaw, cos_yaw, zeros, zeros, zeros, ones), dim=-1
    ).view(-1, 1, 3, 3)
    positions = (world_to_heightmap @ (camera_positions - origin.unsqueeze(1)).unsqueeze(-1)).squeeze(-1)
    return positions, world_to_heightmap @ camera_rotations


def _get_heightmap_grid_shape(env: RslRlVecEnvWrapper, num_rays: int) -> tuple[int, int]:
    pattern_cfg = env.unwrapped.cfg.perceptive_height_scanner.pattern_cfg
    heightmap_cols = int(round(pattern_cfg.size[0] / pattern_cfg.resolution)) + 1
    if num_rays % heightmap_cols != 0:
        heightmap_rows = int(round(pattern_cfg.size[1] / pattern_cfg.resolution)) + 1
    else:
        heightmap_rows = num_rays // heightmap_cols

    if heightmap_rows * heightmap_cols != num_rays:
        raise ValueError(
            f"Could not infer heightmap grid shape from {num_rays} rays and config "
            f"(rows={heightmap_rows}, cols={heightmap_cols})."
        )
    return heightmap_rows, heightmap_cols


def _get_heightmap_targets(env: RslRlVecEnvWrapper, scanner=None) -> tuple[torch.Tensor, tuple[int, int]]:
    scanner = env.unwrapped._perceptive_height_scanner if scanner is None else scanner
    height_data = scanner.data.pos_w[:, 2].unsqueeze(1) - scanner.data.ray_hits_w[..., 2] - HEIGHTMAP_HEIGHT_OFFSET
    height_data = torch.nan_to_num(height_data, nan=0.0, posinf=1.0, neginf=-1.0)
    height_data = height_data.clip(-1.0, 1.0)

    heightmap_rows, heightmap_cols = _get_heightmap_grid_shape(env=env, num_rays=height_data.shape[1])
    heightmaps = height_data.view(height_data.shape[0], 1, heightmap_rows, heightmap_cols)
    return heightmaps, (heightmap_rows, heightmap_cols)


def _default_dataset_path(log_dir: str) -> str:
    return os.path.join(log_dir, "terrain_reconstruction_dataset.pt")


def _maybe_save_checkpoint(
    dataset_builder: TerrainReconstructionDatasetBuilder,
    dataset_path: str,
    metadata: dict,
    collected_rollouts: int,
) -> None:
    if dataset_builder.num_samples == 0:
        return

    checkpoint_path = dataset_path.replace(".pt", f"_rollouts_{collected_rollouts}.pt")
    dataset_builder.save(checkpoint_path, metadata)


@hydra_task_config(args_cli.task, args_cli.agent)
def main(env_cfg: ManagerBasedRLEnvCfg | DirectRLEnvCfg | DirectMARLEnvCfg, agent_cfg: RslRlBaseRunnerCfg):
    """Collect depth/robot-state/heightmap tuples for terrain reconstruction training."""
    task_name = args_cli.task.split(":")[-1]
    train_task_name = task_name.replace("-Play", "")

    agent_cfg = cli_args.update_rsl_rl_cfg(agent_cfg, args_cli)
    agent_cfg = handle_deprecated_rsl_rl_cfg(agent_cfg, importlib_metadata.version("rsl-rl-lib"))
    env_cfg.scene.num_envs = args_cli.num_envs if args_cli.num_envs is not None else env_cfg.scene.num_envs

    env_cfg.seed = agent_cfg.seed
    env_cfg.sim.device = args_cli.device if args_cli.device is not None else env_cfg.sim.device

    log_root_path = os.path.join("logs", "rsl_rl", agent_cfg.experiment_name)
    log_root_path = os.path.abspath(log_root_path)
    print(f"[INFO] Loading experiment from directory: {log_root_path}")
    if args_cli.use_pretrained_checkpoint:
        resume_path = get_published_pretrained_checkpoint("rsl_rl", train_task_name)
        if not resume_path:
            print("[INFO] Unfortunately a pre-trained checkpoint is currently unavailable for this task.")
            return
    elif args_cli.checkpoint:
        resume_path = retrieve_file_path(args_cli.checkpoint)
    else:
        resume_path = get_checkpoint_path(log_root_path, agent_cfg.load_run, agent_cfg.load_checkpoint)

    log_dir = os.path.dirname(resume_path)
    dataset_path = os.path.abspath(args_cli.dataset_path) if args_cli.dataset_path else _default_dataset_path(log_dir)
    env_cfg.log_dir = log_dir
    env_cfg.use_depth_camera = True
    if args_cli.shifted_heightmap_center_x is not None:
        # target-only copy of the policy's height scanner, moved along x: the policy keeps its own observation
        scanner_cfg = env_cfg.perceptive_height_scanner
        env_cfg.reconstruction_target_scanner = scanner_cfg.replace(
            offset=scanner_cfg.offset.replace(pos=(args_cli.shifted_heightmap_center_x, *scanner_cfg.offset.pos[1:])),
            visualizer_cfg=scanner_cfg.visualizer_cfg.replace(prim_path="/Visuals/ReconstructionTargetScanner"),
        )

    env = gym.make(args_cli.task, cfg=env_cfg, render_mode="rgb_array" if args_cli.video else None)

    if isinstance(env.unwrapped, DirectMARLEnv):
        env = multi_agent_to_single_agent(env)

    if args_cli.video:
        video_kwargs = {
            "video_folder": os.path.join(log_dir, "videos", "collect_depth_to_heightmap"),
            "step_trigger": lambda step: step == 0,
            "video_length": args_cli.video_length,
            "disable_logger": True,
        }
        print("[INFO] Recording videos during dataset collection.")
        print_dict(video_kwargs, nesting=4)
        env = gym.wrappers.RecordVideo(env, **video_kwargs)

    env = RslRlVecEnvWrapper(env, clip_actions=agent_cfg.clip_actions)

    print(f"[INFO]: Loading model checkpoint from: {resume_path}")
    if agent_cfg.class_name == "OnPolicyRunner":
        runner = OnPolicyRunner(env, agent_cfg.to_dict(), log_dir=None, device=agent_cfg.device)
    elif agent_cfg.class_name == "DistillationRunner":
        runner = DistillationRunner(env, agent_cfg.to_dict(), log_dir=None, device=agent_cfg.device)
    else:
        raise ValueError(f"Unsupported runner class: {agent_cfg.class_name}")
    runner.load(resume_path)

    policy = runner.get_inference_policy(device=env.unwrapped.device)

    obs = env.get_observations()
    current_depth = _sanitize_depth_data(env)
    current_heightmaps, heightmap_size = _get_heightmap_targets(env)

    num_envs = current_depth.shape[0]
    rollout_horizon = args_cli.rollout_horizon
    if rollout_horizon is None:
        rollout_horizon = int(getattr(env.unwrapped, "max_episode_length", 200))

    if args_cli.depth_history_stride < 1:
        raise ValueError(f"--depth_history_stride must be >= 1, got {args_cli.depth_history_stride}.")
    # every frame of the window is kept on the GPU; only every stride-th one is saved per sample
    depth_window_length = (args_cli.depth_history_length - 1) * args_cli.depth_history_stride + 1
    max_history_length = max(depth_window_length, args_cli.proprio_history_length)
    valid_history_lengths = torch.ones(num_envs, dtype=torch.long, device=env.unwrapped.device)
    depth_dtype = getattr(torch, args_cli.depth_dtype)

    depth_history: deque[torch.Tensor] = deque(maxlen=depth_window_length)
    camera_history: deque[tuple[torch.Tensor, torch.Tensor]] = deque(maxlen=depth_window_length)
    robot_history: deque[torch.Tensor] = deque(maxlen=args_cli.proprio_history_length)
    depth_history.append(current_depth.to(depth_dtype, copy=True))
    camera_history.append(_get_camera_poses(env))
    robot_history.append(obs["common"].clone())
    policy_scanner = env.unwrapped._perceptive_height_scanner
    shifted_scanner = getattr(env.unwrapped, "_reconstruction_target_scanner", None)

    dataset_builder = TerrainReconstructionDatasetBuilder(
        max_samples=args_cli.max_dataset_samples, depth_dtype=depth_dtype
    )
    collected_rollouts = 0
    rollout_step = 0

    depth_camera_cfg = env.unwrapped.cfg.depth_camera
    grid_cfg = env.unwrapped.cfg.perceptive_height_scanner
    metadata = {
        "camera_offset_pos": tuple(depth_camera_cfg.offset.pos),
        "camera_offset_rot_xyzw": tuple(depth_camera_cfg.offset.rot),
        "camera_offset_convention": depth_camera_cfg.offset.convention,
        "camera_focal_length": depth_camera_cfg.pattern_cfg.focal_length,
        "camera_horizontal_aperture": depth_camera_cfg.pattern_cfg.horizontal_aperture,
        # per-sample camera_intrinsics / camera_rotations / camera_positions use the camera frame (x forward, y left,
        # z up) expressed in the current yaw-aligned frame of the policy heightmap scanner. Its origin is the base
        # (RayCaster bakes the offset into the ray starts), so cell (i, j) is centred at (center_x + x_j, y_i).
        "heightmap_grid": {
            "size": tuple(grid_cfg.pattern_cfg.size),
            "resolution": grid_cfg.pattern_cfg.resolution,
            "ordering": grid_cfg.pattern_cfg.ordering,
            "center_x": grid_cfg.offset.pos[0],
        },
        "shifted_heightmap_center_x": args_cli.shifted_heightmap_center_x,
        "heightmap_height_offset": HEIGHTMAP_HEIGHT_OFFSET,
        "depth_max_range": DEPTH_MAX_RANGE,
        "step_dt": env.unwrapped.step_dt,
        "task": args_cli.task,
        "checkpoint_path": resume_path,
        "robot_obs_key": "common",
        "depth_history_length": args_cli.depth_history_length,
        "depth_history_stride": args_cli.depth_history_stride,
        "depth_history_span_steps": depth_window_length - 1,
        "proprio_history_length": args_cli.proprio_history_length,
        "depth_image_size": tuple(current_depth.shape[-2:]),
        "heightmap_size": heightmap_size,
        "num_envs": num_envs,
        "samples_per_step": args_cli.samples_per_step,
        "depth_dtype": args_cli.depth_dtype,
    }

    while (
        simulation_app.is_running()
        and collected_rollouts < args_cli.num_collection_rollouts
        and dataset_builder.num_samples < args_cli.max_dataset_samples
    ):
        with torch.no_grad():
            actions = policy(obs)
            obs, _, dones, _ = env.step(actions)
            dones = dones.bool()

            current_depth = _sanitize_depth_data(env)
            current_heightmaps, _ = _get_heightmap_targets(env)
            current_robot_info = obs["common"].clone()

        valid_history_lengths[dones] = 0
        depth_history.append(current_depth.to(depth_dtype, copy=True))
        camera_history.append(_get_camera_poses(env))
        robot_history.append(current_robot_info)
        valid_history_lengths = torch.clamp(valid_history_lengths + 1, max=max_history_length)

        if len(depth_history) >= depth_window_length and len(robot_history) >= args_cli.proprio_history_length:
            valid_ids = (valid_history_lengths >= max_history_length).nonzero().flatten()
            if args_cli.samples_per_step is not None and valid_ids.numel() > args_cli.samples_per_step:
                valid_ids = valid_ids[torch.randperm(valid_ids.numel(), device=valid_ids.device)[: args_cli.samples_per_step]]
            if valid_ids.numel() > 0:
                # stack the history only for the selected envs instead of all of them
                # newest frame last; walk back from it in steps of the stride
                strided_frames = list(depth_history)[::-args_cli.depth_history_stride][::-1]
                strided_cameras = list(camera_history)[::-args_cli.depth_history_stride][::-1]
                depth_sequence = torch.stack([frame[valid_ids] for frame in strided_frames], dim=1)
                robot_sequence = torch.stack([frame[valid_ids] for frame in robot_history], dim=1)
                camera_positions, camera_rotations = _camera_poses_in_heightmap_frame(
                    camera_positions=torch.stack([pos[valid_ids] for pos, _ in strided_cameras], dim=1),
                    camera_rotations=torch.stack([rot[valid_ids] for _, rot in strided_cameras], dim=1),
                    scanner=policy_scanner,
                    env_ids=valid_ids,
                )
                sample = {
                    "depth_data": depth_sequence,
                    "robot_info": robot_sequence,
                    "heightmaps": current_heightmaps[valid_ids],
                    "camera_intrinsics": _as_torch(env.unwrapped._depth_camera.data.intrinsic_matrices)[valid_ids],
                    "camera_positions": camera_positions,
                    "camera_rotations": camera_rotations,
                    "env_ids": valid_ids,
                }
                if shifted_scanner is not None:
                    sample["heightmaps_shifted"] = _get_heightmap_targets(env, shifted_scanner)[0][valid_ids]
                added_samples = dataset_builder.add_batch(**sample)
                if added_samples > 0 and dataset_builder.num_samples % 1000 < added_samples:
                    print(f"[INFO] Collected {dataset_builder.num_samples} / {args_cli.max_dataset_samples} samples.")

        rollout_step += 1
        if rollout_step >= rollout_horizon:
            collected_rollouts += 1
            rollout_step = 0
            print(
                f"[INFO] Completed rollout {collected_rollouts}/{args_cli.num_collection_rollouts} "
                f"with {dataset_builder.num_samples} saved samples."
            )

            if args_cli.save_every_rollouts > 0 and collected_rollouts % args_cli.save_every_rollouts == 0:
                _maybe_save_checkpoint(
                    dataset_builder=dataset_builder,
                    dataset_path=dataset_path,
                    metadata=metadata,
                    collected_rollouts=collected_rollouts,
                )

    if dataset_builder.num_samples == 0:
        raise RuntimeError("No terrain reconstruction samples were collected. Try increasing rollout count or lowering history lengths.")

    dataset_builder.save(dataset_path, metadata)
    env.close()


if __name__ == "__main__":
    main()
    simulation_app.close()
