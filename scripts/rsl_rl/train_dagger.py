# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Script to play a checkpoint if an RL agent from RSL-RL."""

"""Launch Isaac Sim Simulator first."""

import argparse
import sys

from isaaclab.app import AppLauncher

# local imports
import cli_args  # isort: skip

# add argparse arguments
parser = argparse.ArgumentParser(description="Train an RL agent with RSL-RL.")
parser.add_argument("--video", action="store_true", default=False, help="Record videos during training.")
parser.add_argument("--video_length", type=int, default=200, help="Length of the recorded video (in steps).")
parser.add_argument(
    "--disable_fabric", action="store_true", default=False, help="Disable fabric and use USD I/O operations."
)
parser.add_argument("--num_envs", type=int, default=None, help="Number of environments to simulate.")
parser.add_argument("--task", type=str, default=None, help="Name of the task.")
parser.add_argument(
    "--agent", type=str, default="rsl_rl_cfg_entry_point", help="Name of the RL agent configuration entry point."
)
parser.add_argument("--seed", type=int, default=None, help="Seed used for the environment")
parser.add_argument(
    "--use_pretrained_checkpoint",
    action="store_true",
    help="Use the pre-trained checkpoint from Nucleus.",
)
parser.add_argument("--real-time", action="store_true", default=False, help="Run in real-time, if possible.")
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

import gymnasium as gym
import os
import time
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
from isaaclab.utils.pretrained_checkpoint import get_published_pretrained_checkpoint

from isaaclab_rl.rsl_rl import RslRlBaseRunnerCfg, RslRlVecEnvWrapper, export_policy_as_jit, export_policy_as_onnx

import isaaclab_tasks  # noqa: F401
# Import extensions to set up environment tasks
import basic_locomotion_dls_isaaclab.tasks  # noqa: F401

from isaaclab_tasks.utils import get_checkpoint_path
from isaaclab_tasks.utils.hydra import hydra_task_config

# PLACEHOLDER: Extension template (do not remove this comment)


import torch.nn as nn
import torch.nn.functional as F

class CNNEncoder(nn.Module):
    """
    Encodes an image (B, 1, H, W) -> (B, cnn_dim)
    """
    def __init__(self, cnn_dim: int = 256):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=8, stride=4),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=4, stride=2),
            nn.ReLU(),
            nn.Conv2d(64, 64, kernel_size=3, stride=1),
            nn.ReLU(),
        )
        self.fc = nn.LazyLinear(cnn_dim)

    def forward(self, x):
        x = self.net(x)
        x = x.flatten(1)
        x = self.fc(x)
        return x


class MLPEncoder(nn.Module):
    """
    Encodes numeric features (B, mlp_in) -> (B, mlp_dim)
    """
    def __init__(self, mlp_in: int, mlp_dim: int = 128):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(mlp_in, 128),
            nn.ReLU(),
            nn.Linear(128, mlp_dim),
            nn.ReLU(),
        )

    def forward(self, x):
        return self.net(x)


class DaggerNet(nn.Module):
    """
    Inputs:
      img_seq:  (B, T, C, H, W)
      vec_seq:  (B, T, F)

    Output:
      logits (or actions): (B, T, output_size) if return_sequences=True
                           (B, output_size)   if return_sequences=False (last step)
    """
    def __init__(
        self,
        vec_size: int,
        output_size: int,
        cnn_dim: int = 256,
        mlp_dim: int = 128,
        lstm_hidden: int = 256,
        lstm_layers: int = 1,
        dropout: float = 0.0,
        return_sequences: bool = True,
    ):
        super().__init__()
        self.return_sequences = return_sequences

        self.cnn = CNNEncoder(cnn_dim=cnn_dim)
        self.mlp = MLPEncoder(mlp_in=vec_size, mlp_dim=mlp_dim)

        lstm_in = cnn_dim + mlp_dim
        self.lstm = nn.LSTM(
            input_size=lstm_in,
            hidden_size=lstm_hidden,
            num_layers=lstm_layers,
            batch_first=True,
            dropout=dropout if lstm_layers > 1 else 0.0,
        )

        self.head = nn.Sequential(
            nn.Linear(lstm_hidden, 128),
            nn.ReLU(),
            nn.Linear(128, output_size),
        )

    def forward(self, depth_seq, vec_seq, hidden=None):
        B, T = depth_seq.shape[0], depth_seq.shape[1]

        # CNN per timestep
        depth_flat = depth_seq.reshape(B * T, *depth_seq.shape[2:])  # (B*T, 1, H, W)
        depth_emb = self.cnn(depth_flat).reshape(B, T, -1)           # (B, T, cnn_dim)

        # MLP per timestep
        vec_flat = vec_seq.reshape(B * T, vec_seq.shape[-1])         # (B*T, F)
        vec_emb = self.mlp(vec_flat).reshape(B, T, -1)               # (B, T, mlp_dim)

        # Fuse -> LSTM
        x = torch.cat([depth_emb, vec_emb], dim=-1)                  # (B, T, cnn_dim+mlp_dim)
        lstm_out, new_hidden = self.lstm(x, hidden)                  # (B, T, lstm_hidden)

        if self.return_sequences:
            out = self.head(lstm_out)                                # (B, T, output_size)
        else:
            out = self.head(lstm_out[:, -1])                         # (B, output_size)

        return out, new_hidden
    


@hydra_task_config(args_cli.task, args_cli.agent)
def main(env_cfg: ManagerBasedRLEnvCfg | DirectRLEnvCfg | DirectMARLEnvCfg, agent_cfg: RslRlBaseRunnerCfg):
    """Play with RSL-RL agent."""
    # grab task name for checkpoint path
    task_name = args_cli.task.split(":")[-1]
    train_task_name = task_name.replace("-Play", "")

    # override configurations with non-hydra CLI arguments
    agent_cfg: RslRlBaseRunnerCfg = cli_args.update_rsl_rl_cfg(agent_cfg, args_cli)
    env_cfg.scene.num_envs = args_cli.num_envs if args_cli.num_envs is not None else env_cfg.scene.num_envs

    # set the environment seed
    # note: certain randomizations occur in the environment initialization so we set the seed here
    env_cfg.seed = agent_cfg.seed
    env_cfg.sim.device = args_cli.device if args_cli.device is not None else env_cfg.sim.device

    # specify directory for logging experiments
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

    # set the log directory for the environment (works for all environment types)
    env_cfg.log_dir = log_dir

    # create isaac environment
    env = gym.make(args_cli.task, cfg=env_cfg, render_mode="rgb_array" if args_cli.video else None)

    # convert to single-agent instance if required by the RL algorithm
    if isinstance(env.unwrapped, DirectMARLEnv):
        env = multi_agent_to_single_agent(env)

    # wrap for video recording
    if args_cli.video:
        video_kwargs = {
            "video_folder": os.path.join(log_dir, "videos", "play"),
            "step_trigger": lambda step: step == 0,
            "video_length": args_cli.video_length,
            "disable_logger": True,
        }
        print("[INFO] Recording videos during training.")
        print_dict(video_kwargs, nesting=4)
        env = gym.wrappers.RecordVideo(env, **video_kwargs)

    # wrap around environment for rsl-rl
    env = RslRlVecEnvWrapper(env, clip_actions=agent_cfg.clip_actions)

    print(f"[INFO]: Loading model checkpoint from: {resume_path}")
    # load previously trained model
    if agent_cfg.class_name == "OnPolicyRunner":
        runner = OnPolicyRunner(env, agent_cfg.to_dict(), log_dir=None, device=agent_cfg.device)
    elif agent_cfg.class_name == "DistillationRunner":
        runner = DistillationRunner(env, agent_cfg.to_dict(), log_dir=None, device=agent_cfg.device)
    else:
        raise ValueError(f"Unsupported runner class: {agent_cfg.class_name}")
    runner.load(resume_path)

    # obtain the trained policy for inference
    policy = runner.get_inference_policy(device=env.unwrapped.device)

    # extract the neural network module
    # we do this in a try-except to maintain backwards compatibility.
    try:
        # version 2.3 onwards
        policy_nn = runner.alg.policy
    except AttributeError:
        # version 2.2 and below
        policy_nn = runner.alg.actor_critic

    # extract the normalizer
    if hasattr(policy_nn, "actor_obs_normalizer"):
        normalizer = policy_nn.actor_obs_normalizer
    elif hasattr(policy_nn, "student_obs_normalizer"):
        normalizer = policy_nn.student_obs_normalizer
    else:
        normalizer = None

    # export policy to onnx/jit
    export_model_dir = os.path.join(os.path.dirname(resume_path), "exported")
    export_policy_as_jit(policy_nn, normalizer=normalizer, path=export_model_dir, filename="policy.pt")
    export_policy_as_onnx(policy_nn, normalizer=normalizer, path=export_model_dir, filename="policy.onnx")

    dt = env.unwrapped.step_dt

    from isaaclab.sensors import MultiMeshRayCasterCamera, MultiMeshRayCasterCameraCfg
    env.unwrapped._depth_camera = MultiMeshRayCasterCamera(env.unwrapped.cfg.depth_camera)
    env.unwrapped.scene.sensors["depth_camera"] = env.unwrapped._depth_camera

    # reset environment
    obs = env.get_observations()

    depth_data = env.unwrapped._depth_camera.data.output["distance_to_image_plane"]
    depth_data = torch.nan_to_num(depth_data, nan=0.0, posinf=1.0, neginf=-1.0)
    depth_data = depth_data.clip(-2.0, 2.0)
    
    breakpoint()

    timestep = 0

    num_episodes = 0
    num_steps_per_episode = 200
    states = []
    depths = []
    actions_teacher = []
    dagger_net = DaggerNet(vec_size=obs["common"].shape[1], output_size=env.action_space.shape[1], return_sequences=False).to(env.unwrapped.device)

    # simulate environment
    while simulation_app.is_running():
            
        # run everything in inference mode
        with torch.inference_mode():

            if torch.rand(1) > 0.99/(num_episodes*0.9+1):
                breakpoint()
                predicted_actions, hidden = dagger_net(obs["depth"], obs["common"], hidden=None)
                obs, _, _, _ = env.step(predicted_actions)
            else:
                actions = policy(obs)
                obs, _, _, _ = env.step(actions)
            
            states.append(obs["common"])
            depths.append(obs["depth"])
            actions_teacher.append(actions)

        timestep += 1
        if(timestep % num_steps_per_episode) == 0:
            #train the dagger net
            #TODO: implement training loop here
        
        
            num_episodes += 1
            print(f"[INFO] Completed episode, {num_episodes} remaining.")

    # close the simulator
    env.close()


if __name__ == "__main__":
    # run the main function
    main()
    # close sim app
    simulation_app.close()
