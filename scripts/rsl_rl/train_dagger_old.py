"""Script to play a checkpoint if an RL agent from RSL-RL."""

"""Launch Isaac Sim Simulator first."""

import argparse

from omni.isaac.lab.app import AppLauncher

# local imports
import cli_args  # isort: skip

# add argparse arguments
parser = argparse.ArgumentParser(description="Train an RL agent with RSL-RL.")
parser.add_argument("--cpu", action="store_true", default=False, help="Use CPU pipeline.")
parser.add_argument("--num_envs", type=int, default=None, help="Number of environments to simulate.")
parser.add_argument("--task", type=str, default=None, help="Name of the task.")
parser.add_argument("--seed", type=int, default=None, help="Seed used for the environment")
parser.add_argument("--video", action="store_true", default=False, help="Record videos during training.")
parser.add_argument("--video_length", type=int, default=200, help="Length of the recorded video (in steps).")
parser.add_argument("--video_interval", type=int, default=2000, help="Interval between video recordings (in steps).")

# append RSL-RL cli arguments
cli_args.add_rsl_rl_args(parser)
# append AppLauncher cli args
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()

# launch omniverse app
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

"""Rest everything follows."""


import gymnasium as gym
import os
import torch
import torch.utils.data

from amp_rsl_rl.runners import AMPOnPolicyRunner

import omni.isaac.lab_tasks  # noqa: F401
from omni.isaac.lab_tasks.utils import get_checkpoint_path, parse_env_cfg
from omni.isaac.lab_tasks.utils.wrappers.rsl_rl import (
    RslRlOnPolicyRunnerCfg,
    RslRlVecEnvWrapper,
    export_policy_as_onnx,
)

# Import extensions to set up environment tasks
import amp_ergocub.tasks  # noqa: F401

class DaggerNet(torch.nn.Module):
    def __init__(self, input_size, output_size):
        super(DaggerNet, self).__init__()
        self.fc1 = torch.nn.Linear(input_size, 128)
        self.fc2 = torch.nn.Linear(128, 128)
        self.fc3 = torch.nn.Linear(128, output_size)

    def forward(self, x):
        x = torch.nn.functional.relu(self.fc1(x))
        x = torch.nn.functional.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def current_to_torque(self, obs, current):
        position = obs[6:6+26]
        velocity = obs[6+26:6+26+26]
        torque = 1 * (current - 0.1 * velocity - 0.1 * position)
        return torque

def collect_dagger_data(env, policy, num_episodes=10):
    states = []
    actions = []
    tot_iter = 0
    for _ in range(num_episodes):
        iter = 0
        obs, _ = env.get_observations()
        done = False
        while done is False:
            with torch.inference_mode():
                action = policy(obs)
            next_obs, reward, dones, _ = env.step(action)
            states.append(obs)
            actions.append(action)
            obs = next_obs
            done = bool(torch.any(dones))
            iter += 1
            if done:
                print(f"Done: {done}")

        tot_iter += iter
    print(f"Mean iterations: {tot_iter / num_episodes}")
    # return states and actions as tensors
    return torch.concatenate(states), torch.concatenate(actions)

def select_obs_from_privileged_obs(privileged_obs):
    # 1. base_lin_vel 3
    # 2. base_ang_vel 3
    # 3. projected_gravity 3
    # 4. joint_pos 26
    # 5. joint_vel 26
    # 6. actions 26
    # 7. velocity_commands 3
    # we will select projected_gravity, joint_pos, joint_vel, actions, velocity_commands
    return privileged_obs[:, 6:]

def collect_dagger_data_with_student(env, policy, num_episodes=10):
    states = []
    actions = []
    iter = 0
    for _ in range(num_episodes):
        pr_obs, _ = env.get_observations()
        obs = select_obs_from_privileged_obs(pr_obs)
        done = False
        while done is False:
            with torch.inference_mode():
                action = policy(obs)
            next_obs, reward, dones, _ = env.step(action)
            states.append(obs)
            actions.append(action)
            obs = next_obs
            done = bool(torch.any(dones))
            iter += 1
            if done:
                print(f"Done: {done}")
    # return states and actions as tensors
    return torch.concatenate(states), torch.concatenate(actions)

def dagger_train(dagger_net, policy, env):
    # train the dagger network
    optimizer = torch.optim.Adam(dagger_net.parameters(), lr=1e-3)
    criterion = torch.nn.MSELoss()

    print("Collecting initial data with expert policy.")
    states, actions = collect_dagger_data(env, policy, num_episodes=2)
    print("Finished collecting initial data.")

    num_iterations = 20

    for iteration in range(num_iterations):
        dagger_net.train()
        dataset = torch.utils.data.TensorDataset(states, actions)
        dataloader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)

        for state_batch, action_batch in dataloader:
            optimizer.zero_grad()
            predicted_actions = dagger_net(state_batch)
            loss = criterion(predicted_actions, action_batch)
            loss.backward()
            optimizer.step()

        print(f"Collecting new data with dagger network. Iteration: {iteration}")
        new_states, _ = collect_dagger_data(env, dagger_net, num_episodes=10)
        print("Finished collecting new data.")

        with torch.inference_mode():
            new_actions  = policy(new_states)

        # aggregate new states and actions
        states = torch.cat((states, new_states))
        actions = torch.cat((actions, new_actions))

    # num_iterations = 10
    # for iteration in range(num_iterations):
    #     optimizer.zero_grad()
    #     predicted_actions = dagger_net(states)
    #     loss = criterion(predicted_actions, actions)
    #     loss.backward()
    #     optimizer.step()

    # new_states, _ = collect_dagger_data(env, dagger_net, num_episodes=1)

    # new_actions  = policy(new_states)


def main():
    """Play with RSL-RL agent."""
    # parse configuration
    env_cfg = parse_env_cfg(args_cli.task, use_gpu=not args_cli.cpu, num_envs=args_cli.num_envs)
    agent_cfg: RslRlOnPolicyRunnerCfg = cli_args.parse_rsl_rl_cfg(args_cli.task, args_cli)

    # create isaac environment
    env = gym.make(args_cli.task, cfg=env_cfg, render_mode="rgb_array" if args_cli.video else None)
    # wrap for video recording
    if args_cli.video:
        video_kwargs = {
            "video_folder": "./videos",
            "step_trigger": lambda step: step % args_cli.video_interval == 0,
            "video_length": args_cli.video_length,
            "disable_logger": True,
        }
        print("[INFO] Recording videos during test.")
        env = gym.wrappers.RecordVideo(env, **video_kwargs)
    # wrap around environment for rsl-rl
    env = RslRlVecEnvWrapper(env)

    # specify directory for logging experiments
    log_root_path = os.path.join("logs", "rsl_rl", agent_cfg.experiment_name)
    log_root_path = os.path.abspath(log_root_path)
    print(f"[INFO] Loading experiment from directory: {log_root_path}")
    resume_path = get_checkpoint_path(log_root_path, agent_cfg.load_run, agent_cfg.load_checkpoint)
    print(f"[INFO]: Loading model checkpoint from: {resume_path}")

    # load previously trained model
    ppo_runner = AMPOnPolicyRunner(env, agent_cfg.to_dict(), log_dir=None, device=agent_cfg.device)
    ppo_runner.load(resume_path)
    print(f"[INFO]: Loading model checkpoint from: {resume_path}")

    # obtain the trained policy for inference
    policy = ppo_runner.get_inference_policy(device=env.unwrapped.device)

    # # export policy to onnx
    # export_model_dir = os.path.join(os.path.dirname(resume_path), "exported")
    # export_policy_as_onnx(ppo_runner.alg.actor_critic, export_model_dir, filename="policy.onnx")

    # reset environment
    obs, _ = env.get_observations()
    # simulate environment
    # while simulation_app.is_running():

    dagger_net = DaggerNet(obs.shape[1], env.action_space.shape[1]).to(env.unwrapped.device)

    # train the dagger network
    dagger_train(dagger_net, policy, env)




        # # run everything in inference mode
        # with torch.inference_mode():
        #     # agent stepping
        #     actions = policy(obs)
        #     obs, _, _, _ = env.step(actions)

    # close the simulator
    env.close()


if __name__ == "__main__":
    # run the main execution
    main()
    # close sim app
    simulation_app.close()
