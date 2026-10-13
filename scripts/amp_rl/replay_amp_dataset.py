"""Script to replay an AMP motion dataset kinematically on the robot (no policy, no physics step)."""

"""Launch Isaac Sim Simulator first."""

import argparse
import sys

from isaaclab.app import AppLauncher

# add argparse arguments
parser = argparse.ArgumentParser(description="Replay an AMP motion dataset.")
parser.add_argument("--task", type=str, default="Locomotion-Aliengo-Flat", help="Name of the task.")
parser.add_argument("--dataset", type=str, default="flat", help="Dataset name (file <name>.npy in amp_data_path).")
parser.add_argument("--num_envs", type=int, default=1, help="Number of environments to simulate.")

# append AppLauncher cli args
AppLauncher.add_app_launcher_args(parser)
args_cli, hydra_args = parser.parse_known_args()

# clear out sys.argv for Hydra
sys.argv = [sys.argv[0]] + hydra_args

# launch omniverse app
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

"""Rest everything follows."""


import gymnasium as gym
import numpy as np
import os
import time
import torch

from isaaclab.envs import DirectRLEnvCfg

import isaaclab_tasks  # noqa: F401
from isaaclab_tasks.utils.hydra import hydra_task_config
from isaaclab_rl.rsl_rl import RslRlOnPolicyRunnerCfg

# Import extensions to set up environment tasks
import basic_locomotion_isaaclab.tasks  # noqa: F401


@hydra_task_config(args_cli.task, "rsl_rl_cfg_entry_point")
def main(env_cfg: DirectRLEnvCfg, agent_cfg: RslRlOnPolicyRunnerCfg):
    """Replay the AMP dataset."""
    env_cfg.scene.num_envs = args_cli.num_envs

    # load the dataset from the same folder used for AMP training
    dataset_path = os.path.join(agent_cfg.dataset["amp_data_path"], f"{args_cli.dataset}.npy")
    print(f"[INFO] Replaying AMP dataset: {dataset_path}")
    data = np.load(dataset_path, allow_pickle=True).item()
    # Isaac Lab 3 uses xyzw quaternions, same convention as the dataset (SciPy)
    root_position = np.asarray(data["root_position"], dtype=np.float32)
    root_quaternion = np.asarray(data["root_quaternion"], dtype=np.float32)
    joint_positions = np.asarray(data["joint_positions"], dtype=np.float32)
    dt = 1.0 / data["fps"]

    # create isaac environment
    env = gym.make(args_cli.task, cfg=env_cfg)
    robot = env.unwrapped._robot
    sim = env.unwrapped.sim
    device = env.unwrapped.device
    num_envs = env.unwrapped.num_envs
    env_origins = env.unwrapped._terrain.env_origins

    # map the dataset joint order to the robot joint order
    joint_ids = robot.find_joints(data["joints_list"], preserve_order=True)[0]

    root_velocity = torch.zeros((num_envs, 6), device=device)
    joint_velocity = torch.zeros((num_envs, len(joint_ids)), device=device)

    frame = 0
    # simulate environment
    while simulation_app.is_running():
        start_time = time.time()
        with torch.inference_mode():
            root_pose = torch.zeros((num_envs, 7), device=device)
            root_pose[:, :3] = torch.from_numpy(root_position[frame]).to(device) + env_origins
            root_pose[:, 3:] = torch.from_numpy(root_quaternion[frame]).to(device)
            joint_pos = torch.from_numpy(joint_positions[frame]).to(device).repeat(num_envs, 1)

            robot.write_root_pose_to_sim_index(root_pose=root_pose)
            robot.write_root_velocity_to_sim_index(root_velocity=root_velocity)
            robot.write_joint_position_to_sim_index(position=joint_pos, joint_ids=joint_ids)
            robot.write_joint_velocity_to_sim_index(velocity=joint_velocity, joint_ids=joint_ids)

            # update kinematics and render, without stepping the physics
            sim.forward()
            sim.render()

        # loop over the dataset
        frame = (frame + 1) % len(joint_positions)

        # play the dataset in real time
        sleep_time = dt - (time.time() - start_time)
        if sleep_time > 0:
            time.sleep(sleep_time)

    # close the simulator
    env.close()


if __name__ == "__main__":
    # run the main execution
    main()
    # close sim app
    simulation_app.close()
