import argparse
import sys

from isaaclab.app import AppLauncher

import cli_args  # isort: skip


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "--terrain_model_path", type=str, default=None, help="Terrain reconstructor checkpoint; omit for the true map."
)
parser.add_argument("--task", type=str, default="Locomotion-Go2-Rough-Vision", help="Isaac Lab task to run.")
parser.add_argument("--seed", type=int, default=None, help="Seed used for the environment (terrain).")
parser.add_argument(
    "--draw",
    choices=("tiles", "spheres", "hidden"),
    default="tiles",
    help="tiles: the predicted heightmap coloured by its error; spheres: the prediction alone, as blue spheres; "
    "hidden: nothing drawn. C switches between them while driving.",
)
parser.add_argument(
    "--blind",
    choices=("zeros", "flat"),
    default=None,
    help="The policy gets this map instead of the true or predicted one (the reconstructor still runs and is drawn): "
    "zeros = every cell 0, which in the task's convention (base height - ground height - 0.5 m) is ground 0.5 m below "
    "the base, about 20 cm below where it stands; flat = flat ground at the standing height (no terrain information).",
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
    "--observation_noise",
    action="store_true",
    help="The task's observation noise, as on the robot: the policy and the reconstructor get the same noisy "
    "proprioception; the heightmap is given without noise.",
)
parser.add_argument(
    "--agent", type=str, default="rsl_rl_cfg_entry_point", help="RSL-RL agent configuration entry point."
)
cli_args.add_rsl_rl_args(parser)
AppLauncher.add_app_launcher_args(parser)
args_cli, hydra_args = parser.parse_known_args()
args_cli.enable_cameras = True  # loads the viewport also without a display
sys.argv = [sys.argv[0]] + hydra_args

app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

"""Rest everything follows."""

import importlib.metadata as metadata
import time
from pathlib import Path

import gymnasium as gym
import torch

from isaaclab.devices import Se2Keyboard, Se2KeyboardCfg
from isaaclab.envs import DirectMARLEnv, DirectMARLEnvCfg, DirectRLEnvCfg, ManagerBasedRLEnvCfg, multi_agent_to_single_agent
from isaaclab_rl.rsl_rl import RslRlBaseRunnerCfg, RslRlVecEnvWrapper, handle_deprecated_rsl_rl_cfg
from isaaclab_visualizers.kit import KitVisualizerCfg

import isaaclab_tasks  # noqa: F401
import basic_locomotion_isaaclab.tasks  # noqa: F401
from isaaclab_tasks.utils.hydra import hydra_task_config

import sim_helpers
from terrain_reconstruction_transformer import build_terrain_reconstructor

# command ranges the policy was trained on (custom_events._sample_random_commands): vx, vy (m/s), yaw rate (rad/s)
COMMAND_LIMITS = (1.0, 0.25, 0.8)


@hydra_task_config(args_cli.task, args_cli.agent)
def main(env_cfg: ManagerBasedRLEnvCfg | DirectRLEnvCfg | DirectMARLEnvCfg, agent_cfg: RslRlBaseRunnerCfg):
    checkpoint, model_metadata = None, {}
    if args_cli.terrain_model_path:
        checkpoint = torch.load(args_cli.terrain_model_path, map_location="cpu", weights_only=False)
        model_metadata = checkpoint.get("dataset_metadata", {})

    agent_cfg = cli_args.update_rsl_rl_cfg(agent_cfg, args_cli)
    agent_cfg = handle_deprecated_rsl_rl_cfg(agent_cfg, metadata.version("rsl-rl-lib"))
    env_cfg.scene.num_envs = 1
    env_cfg.seed = agent_cfg.seed
    env_cfg.sim.device = args_cli.device if args_cli.device is not None else env_cfg.sim.device
    env_cfg.external_commands = True  # the keyboard sets the velocity command
    env_cfg.episode_length_s = 3600.0  # no time-out reset while driving
    if not args_cli.observation_noise:
        env_cfg.observation_noise_model = None
    env_cfg.perceptive_height_scanner.debug_vis = False
    if checkpoint is not None:
        sim_helpers.configure_from_checkpoint(env_cfg, model_metadata)
    env_cfg.depth_camera.debug_vis = args_cli.show_depth_rays
    # viewport behind the robot, following it
    env_cfg.sim.visualizer_cfgs = [
        KitVisualizerCfg(eye=(-1.6, -1.2, 1.0), lookat=(0.6, 0.0, 0.0), origin_type="asset", origin_track_path="robot")
    ]
    policy_checkpoint = sim_helpers.policy_checkpoint_path(args_cli, agent_cfg, model_metadata)
    env_cfg.log_dir = str(Path(policy_checkpoint).parent)

    env = gym.make(args_cli.task, cfg=env_cfg)
    if isinstance(env.unwrapped, DirectMARLEnv):
        env = multi_agent_to_single_agent(env)
    env = RslRlVecEnvWrapper(env, clip_actions=agent_cfg.clip_actions)
    policy = sim_helpers.load_policy(env, agent_cfg, policy_checkpoint)
    unwrapped, device = env.unwrapped, env.unwrapped.device

    model = None
    if checkpoint is not None:
        model = build_terrain_reconstructor(checkpoint["model_config"])
        model.load_state_dict(checkpoint["model_state_dict"])
        model.to(device).eval()
        mean, std = checkpoint["target_normalization"]["mean"], checkpoint["target_normalization"]["std"]
        surface = sim_helpers.HeightmapSurface(show_ground_truth=args_cli.show_ground_truth, mode=args_cli.draw)

    keyboard = Se2Keyboard(Se2KeyboardCfg(v_x_sensitivity=COMMAND_LIMITS[0], v_y_sensitivity=COMMAND_LIMITS[1],
                                          omega_z_sensitivity=COMMAND_LIMITS[2], sim_device=device))
    reset_requested = []
    keyboard.add_callback("R", lambda: reset_requested.append(True))
    print(keyboard)
    print("\tReset the robot: R")
    if model is not None:

        def switch_drawing():
            surface.next_mode()
            print(f"[INFO] {sim_helpers.marker_legend(surface.mode, args_cli.show_ground_truth)}")

        keyboard.add_callback("C", switch_drawing)
        print("\tSwitch the heightmap drawing (tiles coloured by error / blue spheres / hidden): C")
        print(f"[INFO] {sim_helpers.marker_legend(surface.mode, args_cli.show_ground_truth)}")
    print(f"[INFO] Policy: {policy_checkpoint}")
    print(f"[INFO] Heightmap: {'predicted by ' + args_cli.terrain_model_path if model else 'true'}"
          + (f", the policy gets a {args_cli.blind} map instead" if args_cli.blind else ""))
    print(f"[INFO] Observation noise: {'on (proprioception)' if args_cli.observation_noise else 'off'}")

    limits = torch.tensor(COMMAND_LIMITS, device=device)
    obs = env.get_observations()
    map_slice = sim_helpers.heightmap_slice(obs, env)
    start_map, blind_map = sim_helpers.true_heightmap(env)[0], None
    if args_cli.blind == "zeros":
        blind_map = torch.zeros_like(start_map)
    elif args_cli.blind == "flat":  # the robots start on flat platforms: the map of the first step is flat ground
        blind_map = torch.full_like(start_map, start_map.mean().item())
    hidden_state, fresh = None, True  # fresh: first step of an episode, skipped by the memory as in its training data
    step_dt = float(unwrapped.step_dt)
    while simulation_app.is_running():
        start_time = time.time()
        with torch.inference_mode():
            unwrapped._commands[:, :3] = torch.maximum(torch.minimum(keyboard.advance().to(device), limits), -limits)
            # the task's noise is on the policy observation only: on the robot both get the same noisy sensors
            proprio = obs["policy"][:, :map_slice.start] if args_cli.observation_noise else obs["common"]
            if model is not None:
                # a fresh step is skipped, as in the training data: flat map, and the memory starts from the next step
                prediction = model(depth_data=sim_helpers.depth_frame(env)[:, None], robot_info=proprio[:, None],
                                   hidden_state=hidden_state)
                hidden_state = None if fresh else prediction.hidden_state
                flat = torch.full_like(obs["policy"][0, map_slice], mean)
                given = flat if fresh else prediction.refined_heightmap.reshape(-1) * std + mean
                surface.update(env, 0, given)
                given = given.clip(-1.0, 1.0)
            else:  # the true map, without the noise
                given = sim_helpers.true_heightmap(env)[0]
            if blind_map is not None:
                given = blind_map
            policy_obs = obs["policy"].clone()
            policy_obs[0, map_slice] = given
            obs["policy"] = policy_obs
            actions = policy(obs)
            obs, _, dones, _ = env.step(actions)
            fresh = bool(dones[0])
            if reset_requested:
                reset_requested.clear()
                obs, _ = env.reset()
                fresh = True
            if hasattr(policy, "reset"):
                policy.reset(dones.bool() | fresh)
        sleep_time = step_dt - (time.time() - start_time)
        if sleep_time > 0.0:
            time.sleep(sleep_time)
    env.close()


if __name__ == "__main__":
    main()
    simulation_app.close()
