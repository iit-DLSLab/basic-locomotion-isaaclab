# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Run a trained depth terrain reconstructor online and display its heightmap with Isaac Lab markers.

The locomotion policy walks and at every step the model gets the inputs it was trained on: the current depth frame and
'common' observation, with its memory carried from the previous step (restarted after each reset). The predicted heightmap is drawn as tiles, one per cell at its predicted height, coloured by the error
against the height scanner: green = close; yellow / orange / red = ground drawn too high (a drop is missed); cyan /
blue / purple = drawn too low. With --draw spheres it is drawn alone instead, as blue spheres at the predicted height.
--show_ground_truth adds small white dots at the true ground. The depth camera is set up as in the checkpoint's data. With --closed_loop the visualized robot's policy walks on the
predicted heightmap instead of the true one. With --record the viewport, following the robot, is written to a video
plus a contact sheet of every --snapshot_interval-th frame, which also works without a display; a few error numbers of
the run are appended to <video dir>/metrics.csv.
"""

"""Launch Isaac Sim Simulator first."""

import argparse
import sys

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
parser.add_argument(
    "--draw",
    choices=("tiles", "spheres"),
    default="tiles",
    help="tiles: the predicted heightmap coloured by its error; spheres: the prediction alone, as blue spheres.",
)
parser.add_argument(
    "--show_ground_truth", action="store_true", help="Also draw small white dots at the true ground height."
)
parser.add_argument(
    "--show_depth_rays",
    action="store_true",
    help="Keep the depth camera's ray-hit debug visualization (red): shows which ground the camera sees.",
)
parser.add_argument(
    "--closed_loop",
    action="store_true",
    help="The visualized robot's policy walks on the predicted heightmap (observation noise off) instead of the true one.",
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
import time
from pathlib import Path

import gymnasium as gym
import torch

from isaaclab.envs import DirectMARLEnv, DirectMARLEnvCfg, DirectRLEnvCfg, ManagerBasedRLEnvCfg, multi_agent_to_single_agent
from isaaclab_rl.rsl_rl import RslRlBaseRunnerCfg, RslRlVecEnvWrapper, handle_deprecated_rsl_rl_cfg

import isaaclab_tasks  # noqa: F401
import basic_locomotion_isaaclab.tasks  # noqa: F401
from isaaclab_tasks.utils.hydra import hydra_task_config

import sim_helpers
from terrain_reconstruction_transformer import build_terrain_reconstructor, heightmap_error_summary


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
    terrain_model = build_terrain_reconstructor(checkpoint["model_config"])
    terrain_model.load_state_dict(checkpoint["model_state_dict"])
    normalization = checkpoint["target_normalization"]
    model_metadata = checkpoint.get("dataset_metadata", {})

    agent_cfg = cli_args.update_rsl_rl_cfg(agent_cfg, args_cli)
    agent_cfg = handle_deprecated_rsl_rl_cfg(agent_cfg, metadata.version("rsl-rl-lib"))
    env_cfg.scene.num_envs = args_cli.num_envs
    env_cfg.seed = agent_cfg.seed
    env_cfg.sim.device = args_cli.device if args_cli.device is not None else env_cfg.sim.device
    sim_helpers.configure_from_checkpoint(env_cfg, model_metadata)
    env_cfg.perceptive_height_scanner.debug_vis = False
    env_cfg.depth_camera.debug_vis = env_cfg.unitree_l2_lidar.debug_vis = args_cli.show_depth_rays
    if args_cli.closed_loop:
        env_cfg.observation_noise_model = None  # the policy gets the predicted map as it is

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

    policy_checkpoint = sim_helpers.policy_checkpoint_path(args_cli, agent_cfg, model_metadata)
    env_cfg.log_dir = str(Path(policy_checkpoint).parent)
    legend = sim_helpers.marker_legend(args_cli.draw, args_cli.show_ground_truth)
    print(f"[INFO] Loading terrain model: {model_path}")
    print(f"[INFO] Loading locomotion policy: {policy_checkpoint}")
    print(
        f"[INFO] Inputs: one depth frame and one observation per step, memory restarted after each reset, "
        f"{checkpoint['model_config'].get('fusion', 'attention')} fusion, commands: {'forward only' if env_cfg.forward_commands else 'default'}, "
        f"policy walks on the {'predicted' if args_cli.closed_loop else 'true'} heightmap"
    )
    print(f"[INFO] Marker colors: {legend}")

    env = gym.make(args_cli.task, cfg=env_cfg)
    if isinstance(env.unwrapped, DirectMARLEnv):
        env = multi_agent_to_single_agent(env)
    env = RslRlVecEnvWrapper(env, clip_actions=agent_cfg.clip_actions)
    policy = sim_helpers.load_policy(env, agent_cfg, policy_checkpoint)

    device = env.unwrapped.device
    terrain_model.to(device).eval()
    surface = sim_helpers.HeightmapSurface(show_ground_truth=args_cli.show_ground_truth, mode=args_cli.draw)
    sensor_frames = sim_helpers.SensorFrames(env, checkpoint["model_config"])
    surface.set_visibility(False)

    # clean_steps counts the visualized env's steps since its last reset
    env_id = args_cli.visualized_env
    clean_steps = 0
    hidden_state = None
    predicted = None  # the latest prediction, for the policy with --closed_loop
    errors: list[torch.Tensor] = []
    obs = env.get_observations()
    map_slice = sim_helpers.heightmap_slice(obs, env)
    step_dt = float(env.unwrapped.step_dt)
    # frames are grabbed from the Kit viewport and written with OpenCV (Isaac Lab's recorder needs MoviePy); the
    # OpenCV of Isaac Sim only has its built-in MJPG encoder, hence .avi
    viewport = None
    video_writer = None
    frames_written = 0
    snapshots = []
    run_name = (
        f"{model_path.stem}{'_closed_loop' if args_cli.closed_loop else ''}{'_spheres' if args_cli.draw == 'spheres' else ''}"
        f"_seed{agent_cfg.seed}_env{env_id}"
    )
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
            if args_cli.closed_loop:
                # the latest prediction, or a flat map while the inputs are not ready (start of an episode)
                given = predicted.reshape(-1) if predicted is not None else torch.full_like(obs["policy"][env_id, map_slice], normalization["mean"])
                policy_obs = obs["policy"].clone()
                policy_obs[env_id, map_slice] = given.clip(-1.0, 1.0)
                obs["policy"] = policy_obs
            actions = policy(obs)
            obs, _, dones, _ = env.step(actions)
            frame = sensor_frames(dones)  # every step: the LiDAR stream follows its messages
            if hasattr(policy, "reset"):
                policy.reset(dones.bool())
            # the reset step itself is dropped too: its sensor data may still show the previous episode
            clean_steps = 0 if dones[env_id] else clean_steps + 1

            if clean_steps > 0:
                if clean_steps == 1:
                    hidden_state = None  # the memory restarts with the episode
                prediction = terrain_model(
                    depth_data=frame[env_id][None, None],
                    robot_info=obs["common"][env_id][None, None],
                    hidden_state=hidden_state,
                )
                hidden_state = prediction.hidden_state
                predicted = prediction.refined_heightmap[0, 0, 0] * normalization["std"] + normalization["mean"]
                errors.append(surface.update(env, env_id, predicted))
                if viewport is not None and frames_written < args_cli.video_length:
                    frame = viewport.render_rgb_array()
                    if frame is not None and frame.any():  # the first viewport frames can be black
                        frame = cv2.cvtColor(frame[..., :3], cv2.COLOR_RGB2BGR)
                        mae_now, mae_run = errors[-1].abs().mean() * 1000, torch.stack(errors).abs().mean() * 1000
                        _annotate(frame, [
                            f"{model_path.stem}  seed {agent_cfg.seed}  step {timestep}"
                            + ("  | the policy walks on this predicted map" if args_cli.closed_loop else ""),
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
                predicted = None
                surface.set_visibility(False)

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
