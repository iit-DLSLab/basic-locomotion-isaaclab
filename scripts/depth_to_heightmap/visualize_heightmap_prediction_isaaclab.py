# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Run a trained depth terrain reconstructor online and display its heightmap with Isaac Lab markers.

The locomotion policy walks and at every step the model gets the inputs it was trained on: the last depth frames with
the checkpoint's stride, the last 'common' observations and, if it has one, its memory across steps (restarted after
each reset). The prediction is drawn as spheres over the terrain, coloured by the error against the height scanner (thresholds
--error_thresholds): green = close; yellow / orange / red = ground drawn too high (a drop is missed); cyan / blue /
purple = drawn too low. The depth camera is set up as in the checkpoint's data. With --record the viewport, following
the robot, is written to a video plus a contact sheet of every --snapshot_interval-th frame, which also works without
a display; a few error numbers of the run are appended to <video dir>/metrics.csv.
"""

"""Launch Isaac Sim Simulator first."""

import argparse
import sys
from collections import deque

from isaaclab.app import AppLauncher

import cli_args  # isort: skip


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "--terrain_model_path",
    "--model_path",
    dest="terrain_model_path",
    required=True,
    help="Checkpoint produced by terrain_reconstruction_transformer.py.",
)
parser.add_argument("--task", type=str, default="Locomotion-Go2-Rough-Vision", help="Isaac Lab task to run.")
parser.add_argument("--num_envs", type=int, default=1, help="Number of simulated environments.")
parser.add_argument("--visualized_env", type=int, default=0, help="Environment whose prediction is displayed.")
parser.add_argument("--marker_radius", type=float, default=0.02, help="Prediction marker sphere radius in metres.")
parser.add_argument(
    "--error_thresholds",
    type=float,
    nargs=3,
    default=(0.01, 0.03, 0.05),
    help="Height errors in metres between the marker colours: green below the first, then 3 shades above / below.",
)
parser.add_argument(
    "--show_ground_truth",
    action="store_true",
    help="Also display smaller white markers at the height-scanner target positions.",
)
parser.add_argument(
    "--show_depth_rays",
    action="store_true",
    help="Keep the depth camera's ray-hit debug visualization (red): shows which ground the camera sees.",
)
parser.add_argument("--metrics_interval", type=int, default=50, help="Print the MAE every N steps. 0 disables it.")
parser.add_argument("--max_steps", type=int, default=0, help="Stop after N simulation steps. 0 runs indefinitely.")
parser.add_argument("--record", action="store_true", default=False, help="Record the viewport, following the robot, to a video.")
parser.add_argument("--video_length", type=int, default=300, help="Frames to record.")
parser.add_argument(
    "--video_dir", type=str, default=None, help="Output folder of the video. Defaults to <model dir>/videos."
)
parser.add_argument("--snapshot_interval", type=int, default=50, help="With --record, every N-th frame goes in the contact sheet.")
parser.add_argument("--real-time", action="store_true", default=False, help="Run in real time, if possible.")
parser.add_argument("--seed", type=int, default=None, help="Seed used for the environment.")
parser.add_argument(
    "--agent", type=str, default="rsl_rl_cfg_entry_point", help="RSL-RL agent configuration entry point."
)
parser.add_argument(
    "--use_pretrained_checkpoint",
    action="store_true",
    help="Use the published locomotion-policy checkpoint instead of the one recorded in the model metadata.",
)
cli_args.add_rsl_rl_args(parser)
AppLauncher.add_app_launcher_args(parser)
args_cli, hydra_args = parser.parse_known_args()

if not 0 <= args_cli.visualized_env < args_cli.num_envs:
    raise ValueError("--visualized_env must be in [0, num_envs).")
if args_cli.record:
    args_cli.enable_cameras = True

sys.argv = [sys.argv[0]] + hydra_args

app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

"""Rest everything follows."""

import importlib.metadata as metadata
import os
import time
from pathlib import Path

import gymnasium as gym
import torch
from rsl_rl.runners import DistillationRunner, OnPolicyRunner

import isaaclab.sim as sim_utils
from isaaclab.envs import (
    DirectMARLEnv,
    DirectMARLEnvCfg,
    DirectRLEnvCfg,
    ManagerBasedRLEnvCfg,
    multi_agent_to_single_agent,
)
from isaaclab.markers import VisualizationMarkers, VisualizationMarkersCfg
from isaaclab.utils.assets import retrieve_file_path
from isaaclab_rl.rsl_rl import RslRlBaseRunnerCfg, RslRlVecEnvWrapper, handle_deprecated_rsl_rl_cfg
from isaaclab_rl.utils.pretrained_checkpoint import get_published_pretrained_checkpoint

import isaaclab_tasks  # noqa: F401
import basic_locomotion_isaaclab.tasks  # noqa: F401
from isaaclab_tasks.utils import get_checkpoint_path
from isaaclab_tasks.utils.hydra import hydra_task_config

from terrain_reconstruction_transformer import MultiModalTerrainReconstructor, heightmap_error_summary

# as in collect_depth_to_heightmap.py
HEIGHTMAP_HEIGHT_OFFSET = 0.5
DEPTH_MAX_RANGE = 2.0


def _as_torch(value) -> torch.Tensor:
    return value.torch if hasattr(value, "torch") else value


def _depth_frame(env: RslRlVecEnvWrapper) -> torch.Tensor:
    """(num_envs, 1, H, W), invalid rays = 0, clipped to the training range."""
    depth = _as_torch(env.unwrapped._depth_camera.data.output["distance_to_image_plane"])
    depth = torch.nan_to_num(depth, nan=0.0, posinf=0.0, neginf=0.0).clip(0.0, DEPTH_MAX_RANGE)
    return depth.permute(0, 3, 1, 2)


def _create_markers(marker_radius: float, show_ground_truth: bool) -> tuple[VisualizationMarkers, VisualizationMarkers | None]:
    def sphere(radius: float, color: tuple[float, float, float]) -> sim_utils.SphereCfg:
        return sim_utils.SphereCfg(radius=radius, visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=color))

    # the order matches the indices of _update_markers: 0 close, 1-3 too high, 4-6 too low (growing error)
    prediction_markers = VisualizationMarkers(
        VisualizationMarkersCfg(
            prim_path="/Visuals/DepthHeightmapPrediction",
            markers={
                "close": sphere(marker_radius, (0.1, 0.9, 0.1)),
                "high_1": sphere(marker_radius, (1.0, 0.9, 0.1)),
                "high_2": sphere(marker_radius, (1.0, 0.5, 0.05)),
                "high_3": sphere(marker_radius, (0.9, 0.05, 0.05)),
                "low_1": sphere(marker_radius, (0.2, 0.9, 1.0)),
                "low_2": sphere(marker_radius, (0.1, 0.35, 1.0)),
                "low_3": sphere(marker_radius, (0.5, 0.1, 0.8)),
            },
        )
    )
    target_markers = None
    if show_ground_truth:
        target_markers = VisualizationMarkers(
            VisualizationMarkersCfg(
                prim_path="/Visuals/DepthHeightmapTarget",
                markers={"target": sphere(max(marker_radius * 0.45, 0.005), (1.0, 1.0, 1.0))},
            )
        )
    return prediction_markers, target_markers


def _update_markers(
    env: RslRlVecEnvWrapper,
    predicted: torch.Tensor,
    prediction_markers: VisualizationMarkers,
    target_markers: VisualizationMarkers | None,
) -> torch.Tensor:
    """Place the markers of the visualized env (predicted heightmap (rows, cols), metres); returns the height error."""
    scanner = env.unwrapped._perceptive_height_scanner
    sensor_z = _as_torch(scanner.data.pos_w)[args_cli.visualized_env, 2]
    ray_hits = _as_torch(scanner.data.ray_hits_w)[args_cli.visualized_env]
    # the heightmap stores sensor height - ground height - offset, with the scanner rays in the same order
    predicted_z = sensor_z - predicted.reshape(-1) - HEIGHTMAP_HEIGHT_OFFSET
    target_z = ray_hits[:, 2]
    # spheres drawn resting on the surface, not half buried in it
    lift = torch.tensor([0.0, 0.0, args_cli.marker_radius], device=ray_hits.device)
    predicted_positions = torch.cat((ray_hits[:, :2], predicted_z.unsqueeze(1)), dim=1) + lift
    target_positions = ray_hits + lift
    valid = torch.isfinite(predicted_positions).all(dim=1) & torch.isfinite(target_positions).all(dim=1)

    error = predicted_z - target_z
    level = sum((error.abs() >= threshold).long() for threshold in args_cli.error_thresholds)  # 0 .. 3
    marker_indices = torch.where(error >= 0, level, torch.where(level > 0, level + 3, 0))
    prediction_markers.visualize(translations=predicted_positions[valid], marker_indices=marker_indices[valid])
    if target_markers is not None:
        target_markers.visualize(translations=target_positions[valid])
    return error.view_as(predicted)


def _annotate(frame, lines: list[str]):
    """Write text lines on the top left of a BGR frame, white on a dark band."""
    import cv2

    for row, text in enumerate(lines):
        origin = (12, 28 + 26 * row)
        cv2.putText(frame, text, origin, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (20, 20, 20), 4, cv2.LINE_AA)
        cv2.putText(frame, text, origin, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
    return frame


@hydra_task_config(args_cli.task, args_cli.agent)
def main(env_cfg: ManagerBasedRLEnvCfg | DirectRLEnvCfg | DirectMARLEnvCfg, agent_cfg: RslRlBaseRunnerCfg):
    """Run locomotion, terrain inference and marker visualization."""
    model_path = Path(args_cli.terrain_model_path).expanduser().resolve()
    checkpoint = torch.load(model_path, map_location="cpu", weights_only=False)
    terrain_model = MultiModalTerrainReconstructor(**checkpoint["model_config"])
    terrain_model.load_state_dict(checkpoint["model_state_dict"])
    normalization = checkpoint["target_normalization"]
    model_metadata = checkpoint.get("dataset_metadata", {})
    depth_history_length = int(model_metadata.get("depth_history_length", 5))
    depth_history_stride = int(model_metadata.get("depth_history_stride", 1))
    proprio_history_length = int(model_metadata.get("proprio_history_length", 50))
    # steps t-K .. t of one episode are needed, as for the training windows
    history = max((depth_history_length - 1) * depth_history_stride, proprio_history_length - 1)

    task_name = args_cli.task.split(":")[-1]
    train_task_name = task_name.replace("-Play", "")
    agent_cfg = cli_args.update_rsl_rl_cfg(agent_cfg, args_cli)
    agent_cfg = handle_deprecated_rsl_rl_cfg(agent_cfg, metadata.version("rsl-rl-lib"))
    env_cfg.scene.num_envs = args_cli.num_envs
    env_cfg.seed = agent_cfg.seed
    env_cfg.sim.device = args_cli.device if args_cli.device is not None else env_cfg.sim.device
    env_cfg.use_depth_camera = True
    env_cfg.perceptive_height_scanner.debug_vis = False
    env_cfg.depth_camera.debug_vis = args_cli.show_depth_rays

    # the depth camera of the training data
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

    video_dir = Path(args_cli.video_dir or model_path.parent / "videos")
    if args_cli.record:
        from isaaclab_visualizers.kit import KitVisualizerCfg

        # chase view: behind and to the right of the robot, looking at the heightmap in front of it
        env_cfg.sim.visualizer_cfgs = [
            KitVisualizerCfg(
                eye=(-1.3, -1.3, 0.9),
                lookat=(0.5, 0.0, 0.0),
                origin_type="asset",
                origin_track_path="robot",
                origin_env_index=args_cli.visualized_env,
            )
        ]

    if args_cli.use_pretrained_checkpoint:
        policy_checkpoint = get_published_pretrained_checkpoint("rsl_rl", train_task_name)
    elif args_cli.checkpoint:
        policy_checkpoint = retrieve_file_path(args_cli.checkpoint)
    elif Path(str(model_metadata.get("checkpoint_path", ""))).is_file():
        policy_checkpoint = str(model_metadata["checkpoint_path"])
    else:
        log_root_path = os.path.abspath(os.path.join("logs", "rsl_rl", agent_cfg.experiment_name))
        policy_checkpoint = get_checkpoint_path(log_root_path, agent_cfg.load_run, agent_cfg.load_checkpoint)
    env_cfg.log_dir = os.path.dirname(policy_checkpoint)
    print(f"[INFO] Loading terrain model: {model_path}")
    print(f"[INFO] Loading locomotion policy: {policy_checkpoint}")
    print(
        f"[INFO] Inputs: {depth_history_length} depth frames every {depth_history_stride} steps, "
        f"{proprio_history_length} proprio steps, memory across steps: {terrain_model.recurrent_steps}"
    )
    t1, t2, t3 = (round(threshold * 100) for threshold in args_cli.error_thresholds)
    legend = f"green <{t1} cm | too high: yellow {t1}-{t2}, orange {t2}-{t3}, red >{t3} | too low: cyan, blue, purple"
    print(f"[INFO] Marker colors: {legend}")

    env = gym.make(args_cli.task, cfg=env_cfg)
    if isinstance(env.unwrapped, DirectMARLEnv):
        env = multi_agent_to_single_agent(env)
    env = RslRlVecEnvWrapper(env, clip_actions=agent_cfg.clip_actions)

    if agent_cfg.class_name == "OnPolicyRunner":
        runner = OnPolicyRunner(env, agent_cfg.to_dict(), log_dir=None, device=agent_cfg.device)
    elif agent_cfg.class_name == "DistillationRunner":
        runner = DistillationRunner(env, agent_cfg.to_dict(), log_dir=None, device=agent_cfg.device)
    else:
        raise ValueError(f"Unsupported runner class: {agent_cfg.class_name}")
    runner.load(policy_checkpoint)
    policy = runner.get_inference_policy(device=env.unwrapped.device)

    device = env.unwrapped.device
    terrain_model.to(device).eval()
    prediction_markers, target_markers = _create_markers(args_cli.marker_radius, args_cli.show_ground_truth)
    prediction_markers.set_visibility(False)

    # the visualized env's last history + 1 steps; clean_steps counts the steps since its last reset
    env_id = args_cli.visualized_env
    depth_frames: deque[torch.Tensor] = deque(maxlen=history + 1)
    proprio_frames: deque[torch.Tensor] = deque(maxlen=history + 1)
    clean_steps = 0
    hidden_state = None
    errors: list[torch.Tensor] = []
    obs = env.get_observations()
    step_dt = float(env.unwrapped.step_dt)
    # frames are grabbed from the Kit viewport and written with OpenCV (Isaac Lab's recorder needs MoviePy); the
    # OpenCV of Isaac Sim only has its built-in MJPG encoder, hence .avi
    viewport = None
    video_writer = None
    frames_written = 0
    snapshots = []
    run_name = f"{model_path.stem}_seed{agent_cfg.seed}_env{env_id}"
    if args_cli.record:
        import cv2
        import numpy as np
        import omni.usd
        from pxr import UsdGeom

        # several envs can share a terrain tile and walk through each other: show only the visualized robot (the depth
        # camera only sees the terrain, so this changes nothing for the model)
        stage = omni.usd.get_context().get_stage()
        for other in range(env.unwrapped.num_envs):
            if other != env_id:
                UsdGeom.Imageable(stage.GetPrimAtPath(f"/World/envs/env_{other}/Robot")).MakeInvisible()

        viewport = next(v for v in env.unwrapped.sim.visualizers if getattr(v.cfg, "visualizer_type", None) == "kit")
        video_dir.mkdir(parents=True, exist_ok=True)
        video_path = video_dir / f"{run_name}.avi"
    timestep = 0
    while simulation_app.is_running():
        start_time = time.time()
        with torch.inference_mode():
            actions = policy(obs)
            obs, _, dones, _ = env.step(actions)
            if hasattr(policy, "reset"):
                policy.reset(dones.bool())
            # the reset step itself is dropped too: its sensor data may still show the previous episode
            clean_steps = 0 if dones[env_id] else clean_steps + 1
            depth_frames.append(_depth_frame(env)[env_id].clone())
            proprio_frames.append(obs["common"][env_id].clone())

            if clean_steps > history:
                if clean_steps == history + 1:
                    hidden_state = None  # the memory restarts with the episode
                depth = torch.stack(
                    [depth_frames[-1 - (depth_history_length - 1 - j) * depth_history_stride] for j in range(depth_history_length)]
                )
                robot_info = torch.stack(list(proprio_frames)[-proprio_history_length:])
                prediction = terrain_model(depth_data=depth[None], robot_info=robot_info[None], hidden_state=hidden_state)
                hidden_state = prediction.hidden_state
                predicted = prediction.refined_heightmap[0, 0] * normalization["std"] + normalization["mean"]
                prediction_markers.set_visibility(True)
                if target_markers is not None:
                    target_markers.set_visibility(True)
                errors.append(_update_markers(env, predicted, prediction_markers, target_markers))
                if viewport is not None and frames_written < args_cli.video_length:
                    frame = viewport.render_rgb_array()
                    if frame is not None and frame.any():  # the first viewport frames can be black
                        frame = cv2.cvtColor(frame[..., :3], cv2.COLOR_RGB2BGR)
                        mae_now, mae_run = errors[-1].abs().mean() * 1000, torch.stack(errors).abs().mean() * 1000
                        _annotate(frame, [
                            f"{model_path.stem}  seed {agent_cfg.seed}  step {timestep}",
                            f"MAE now {mae_now:.1f} mm, so far {mae_run:.1f} mm",
                            legend,
                        ])
                        if video_writer is None:
                            size = (frame.shape[1], frame.shape[0])
                            fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                            video_writer = cv2.VideoWriter(str(video_path), fourcc, round(1.0 / step_dt), size)
                            if not video_writer.isOpened():
                                raise RuntimeError(f"OpenCV cannot write {video_path}")
                            video_writer.set(cv2.VIDEOWRITER_PROP_QUALITY, 80)  # MJPG: smaller files
                        video_writer.write(frame)
                        if args_cli.snapshot_interval > 0 and frames_written % args_cli.snapshot_interval == 0:
                            snapshots.append(cv2.resize(frame, (frame.shape[1] // 2, frame.shape[0] // 2)))
                        frames_written += 1
                if args_cli.metrics_interval > 0 and len(errors) % args_cli.metrics_interval == 0:
                    recent = torch.stack(errors[-args_cli.metrics_interval :]).abs().mean()
                    print(f"[METRICS] step={timestep} env={env_id} MAE last {args_cli.metrics_interval} steps: {recent * 1000:.1f} mm")
            else:
                prediction_markers.set_visibility(False)
                if target_markers is not None:
                    target_markers.set_visibility(False)
                if clean_steps == 0 or timestep == 0:
                    print(f"[INFO] Filling the input history of env {env_id}: {history + 1 - clean_steps} steps.")

        timestep += 1
        if args_cli.max_steps > 0 and timestep >= args_cli.max_steps:
            break
        sleep_time = step_dt - (time.time() - start_time)
        if args_cli.real_time and sleep_time > 0.0:
            time.sleep(sleep_time)

    if errors:
        summary = heightmap_error_summary(torch.stack(errors).cpu())
        print("[INFO] " + ", ".join(f"{key} {value:.2f}" for key, value in summary.items()))
        if args_cli.record:
            metrics_path = video_dir / "metrics.csv"
            row = {"run": run_name, **{key: f"{value:.2f}" for key, value in summary.items()}}
            with open(metrics_path, "a") as file:
                if file.tell() == 0:
                    file.write(",".join(row) + "\n")
                file.write(",".join(str(value) for value in row.values()) + "\n")
            print(f"[INFO] Metrics appended to: {metrics_path}")
    if video_writer is not None:
        video_writer.release()
        print(f"[INFO] {frames_written} frames written to: {video_path}")
    if snapshots:
        # contact sheet, two snapshots per row
        if len(snapshots) % 2:
            snapshots.append(np.zeros_like(snapshots[0]))
        sheet = np.vstack([np.hstack(snapshots[i : i + 2]) for i in range(0, len(snapshots), 2)])
        cv2.imwrite(str(video_dir / f"{run_name}_sheet.png"), sheet)
    env.close()


if __name__ == "__main__":
    main()
    simulation_app.close()
