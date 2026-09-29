# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Collect terrain reconstruction sequences with a trained locomotion policy.

Every step of every env is recorded (one depth frame, the 'common' observation, the heightmap target, the reset flag
and the camera/scanner poses) and written time-major, ``(steps, envs, ...)``, to chunk files in ``--dataset_path``.
History windows and depth strides are built at training time from these sequences.
"""

"""Launch Isaac Sim Simulator first."""

import argparse
import os
import sys

from isaaclab.app import AppLauncher

# local imports
import cli_args  # isort: skip

# add argparse arguments
parser = argparse.ArgumentParser(description="Collect terrain reconstruction sequences with a trained RSL-RL policy.")
parser.add_argument("--video", action="store_true", default=False, help="Record videos during collection.")
parser.add_argument("--video_length", type=int, default=200, help="Length of the recorded video (in steps).")
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
parser.add_argument(
    "--dataset_path",
    type=str,
    default=None,
    help="Directory for the chunk files. Defaults to <checkpoint_dir>/terrain_reconstruction_sequences.",
)
parser.add_argument("--num_steps", type=int, default=1200, help="Steps to record; every env is recorded at every step.")
parser.add_argument(
    "--steps_per_chunk",
    type=int,
    default=100,
    help="Steps per chunk file (all envs). With 256 envs a step of fp16 depth is about 13 MB.",
)
parser.add_argument(
    "--depth_dtype",
    type=str,
    choices=("float16", "float32"),
    default="float16",
    help="Storage dtype for depth frames. float16 halves the dataset memory (~1 mm precision in the 0-2 m range).",
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


class SequenceChunkWriter:
    """Every step of every env, time-major ``(steps, envs, ...)``, written to disk in chunks so RAM stays bounded.

    Each step is copied to the CPU right away: Isaac Lab reuses its observation and sensor buffers in place, so
    keeping references would store the same buffer many times.
    """

    def __init__(self, directory: str, steps_per_chunk: int, depth_dtype: torch.dtype, metadata: dict):
        self.directory = directory
        self.steps_per_chunk = steps_per_chunk
        self.depth_dtype = depth_dtype
        self.metadata = metadata
        self.steps: dict[str, list[torch.Tensor]] = {}
        self.num_steps = 0
        self.chunk_index = 0
        self.chunk_first_step = 0
        os.makedirs(directory, exist_ok=True)

    def add_step(self, **tensors: torch.Tensor) -> None:
        for name, tensor in tensors.items():
            tensor = tensor.detach().to(self.depth_dtype) if name == "depth_data" else tensor.detach()
            self.steps.setdefault(name, []).append(tensor.to("cpu", copy=True))
        self.num_steps += 1
        if self.num_steps - self.chunk_first_step == self.steps_per_chunk:
            self.flush()

    def flush(self) -> None:
        if not self.steps:
            return
        chunk = {name: torch.stack(steps) for name, steps in self.steps.items()}
        chunk["metadata"] = {
            **self.metadata,
            "chunk_index": self.chunk_index,
            "first_step": self.chunk_first_step,
            "num_steps": self.num_steps - self.chunk_first_step,
        }
        path = os.path.join(self.directory, f"chunk_{self.chunk_index:03d}.pt")
        torch.save(chunk, path)
        print(f"[INFO] Saved steps {self.chunk_first_step}-{self.num_steps - 1} to: {path}")
        self.steps = {}
        self.chunk_index += 1
        self.chunk_first_step = self.num_steps


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


def _get_heightmap_targets(env: RslRlVecEnvWrapper) -> torch.Tensor:
    """Policy heightmap as (num_envs, 1, rows, cols): rows along y (lateral), cols along x (forward)."""
    scanner = env.unwrapped._perceptive_height_scanner
    height_data = scanner.data.pos_w[:, 2].unsqueeze(1) - scanner.data.ray_hits_w[..., 2] - HEIGHTMAP_HEIGHT_OFFSET
    height_data = torch.nan_to_num(height_data, nan=0.0, posinf=1.0, neginf=-1.0)
    height_data = height_data.clip(-1.0, 1.0)

    heightmap_rows, heightmap_cols = _get_heightmap_grid_shape(env=env, num_rays=height_data.shape[1])
    return height_data.view(height_data.shape[0], 1, heightmap_rows, heightmap_cols)


@hydra_task_config(args_cli.task, args_cli.agent)
def main(env_cfg: ManagerBasedRLEnvCfg | DirectRLEnvCfg | DirectMARLEnvCfg, agent_cfg: RslRlBaseRunnerCfg):
    """Record every step of every env for ``--num_steps`` steps.

    Per step and env: ``depth_data`` (1, H, W), ``robot_info`` (the 'common' observation), ``heightmaps`` (1, rows,
    cols), ``dones`` (the episode ended at this step: Isaac Lab has already reset the env, so this step belongs to
    the next episode), and the world pose of the camera and of the heightmap scanner (to rebuild relative poses
    later). A training window over steps t-K..t is valid only if none of them has ``dones``: this also drops the
    reset step itself, whose sensor data may still show the previous episode. Episodes shorter than K+1 steps give
    no windows.
    """
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
    if args_cli.dataset_path:
        dataset_dir = os.path.abspath(args_cli.dataset_path)
    else:
        dataset_dir = os.path.join(log_dir, "terrain_reconstruction_sequences")
    env_cfg.log_dir = log_dir
    env_cfg.use_depth_camera = True

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

    depth_camera_cfg = env.unwrapped.cfg.depth_camera
    grid_cfg = env.unwrapped.cfg.perceptive_height_scanner
    scanner = env.unwrapped._perceptive_height_scanner
    metadata = {
        "format": "sequence",
        "camera_offset_pos": tuple(depth_camera_cfg.offset.pos),
        "camera_offset_rot_xyzw": tuple(depth_camera_cfg.offset.rot),
        "camera_offset_convention": depth_camera_cfg.offset.convention,
        "camera_focal_length": depth_camera_cfg.pattern_cfg.focal_length,
        "camera_horizontal_aperture": depth_camera_cfg.pattern_cfg.horizontal_aperture,
        # the same for every env and step
        "camera_intrinsics": _as_torch(env.unwrapped._depth_camera.data.intrinsic_matrices)[0].cpu(),
        "heightmap_grid": {
            "size": tuple(grid_cfg.pattern_cfg.size),
            "resolution": grid_cfg.pattern_cfg.resolution,
            "ordering": grid_cfg.pattern_cfg.ordering,
            "center_x": grid_cfg.offset.pos[0],
        },
        "heightmap_height_offset": HEIGHTMAP_HEIGHT_OFFSET,
        "depth_max_range": DEPTH_MAX_RANGE,
        "step_dt": env.unwrapped.step_dt,
        "task": args_cli.task,
        "checkpoint_path": resume_path,
        "seed": agent_cfg.seed,
        "robot_obs_key": "common",
        "depth_image_size": tuple(_sanitize_depth_data(env).shape[-2:]),
        "heightmap_size": tuple(_get_heightmap_targets(env).shape[-2:]),
        "num_envs": env.unwrapped.num_envs,
        "sequence_steps": args_cli.num_steps,
        "steps_per_chunk": args_cli.steps_per_chunk,
        "depth_dtype": args_cli.depth_dtype,
    }
    writer = SequenceChunkWriter(
        directory=dataset_dir,
        steps_per_chunk=args_cli.steps_per_chunk,
        depth_dtype=getattr(torch, args_cli.depth_dtype),
        metadata=metadata,
    )

    while simulation_app.is_running() and writer.num_steps < args_cli.num_steps:
        with torch.no_grad():
            actions = policy(obs)
            obs, _, dones, _ = env.step(actions)
            camera_positions, camera_rotations = _get_camera_poses(env)
            writer.add_step(
                depth_data=_sanitize_depth_data(env),
                robot_info=obs["common"],
                heightmaps=_get_heightmap_targets(env),
                dones=dones.bool(),
                camera_positions_w=camera_positions,
                camera_rotations_w=camera_rotations,
                scanner_positions_w=_as_torch(scanner.data.pos_w),
                scanner_quats_w=_as_torch(scanner.data.quat_w),
            )
        if writer.num_steps % 100 == 0:
            print(f"[INFO] Recorded {writer.num_steps} / {args_cli.num_steps} steps.")

    writer.flush()
    print(f"[INFO] Saved {writer.num_steps} steps x {metadata['num_envs']} envs in {writer.chunk_index} chunks to: {dataset_dir}")
    env.close()


if __name__ == "__main__":
    main()
    simulation_app.close()
