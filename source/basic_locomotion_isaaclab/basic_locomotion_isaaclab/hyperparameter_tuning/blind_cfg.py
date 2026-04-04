# Copyright (c) 2022-2025, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import pathlib
import sys

# Allow for import of items from the ray workflow.
UTIL_DIR = pathlib.Path(__file__).parent.parent.parent
sys.path.append(str(UTIL_DIR))
import tuner
import util
from ray import tune


class BlindJobCfg(tuner.JobCfg):
    """In order to be compatible with :meth: invoke_tuning_run, and
    :class:IsaacLabTuneTrainable , configurations should
    be in a similar format to this class. This class can vary env count/horizon length,
    CNN structure, and MLP structure. Broad possible ranges are set, the specific values
    that work can be found via tuning. Tuning results can inform better ranges for a second tuning run.
    These ranges were selected for demonstration purposes. Best ranges are run/task specific."""

    @staticmethod
    def _get_batch_size_divisors(batch_size: int, min_size: int = 128) -> list[int]:
        """Get valid batch divisors to combine with num_envs and horizon length"""
        divisors = [i for i in range(min_size, batch_size + 1) if batch_size % i == 0]
        return divisors if divisors else [min_size]

    def __init__(self, cfg={}, vary_env_count: bool = False, vary_mlp_param: bool = False, vary_networks_type: bool = False, vary_algorithm_param: bool = False):
        cfg = util.populate_isaac_ray_cfg_args(cfg)

        # Basic configuration
        cfg["runner_args"]["headless_singleton"] = "--headless"
        
        # RSL-RL specific configurations
        cfg["hydra_args"]["agent.max_iterations"] = 2000
        if vary_env_count:  
            env_counts = [4096]
            horizon_lengths = [16, 24, 32, 40]

            selected_env_count = tune.choice(env_counts)
            selected_horizon = tune.choice(horizon_lengths)

            cfg["runner_args"]["--num_envs"] = selected_env_count
            cfg["hydra_args"]["agent.num_steps_per_env"] = selected_horizon

        
        if vary_mlp_param:
            max_num_layers = 3
            #num_layers = tune.randint(3, max_num_layers)
            neurons_per_layer = [64, 128, 256]
            num_layers = 3

            def get_mlp_layers(_):
                return [tune.choice(neurons_per_layer).sample() for _ in range(num_layers)]


            cfg["hydra_args"]["agent.policy.actor_hidden_dims"] = tune.sample_from(get_mlp_layers)
            cfg["hydra_args"]["agent.policy.critic_hidden_dims"] = tune.sample_from(get_mlp_layers)
            cfg["hydra_args"]["agent.policy.activation"] = tune.choice(
                ["relu", "tanh", "sigmoid", "elu"]
            )
        
        if vary_networks_type:
            cfg["hydra_args"]["agent.policy.class_name"] = tune.choice(["ActorCriticRecurrent", "ActorCritic"])

        if vary_algorithm_param:
            cfg["hydra_args"]["agent.algorithm.clip_param"] = tune.choice([0.1, 0.15, 0.2, 0.25, 0.3])
            cfg["hydra_args"]["agent.algorithm.entropy_coef"] = tune.choice([0.005, 0.01, 0.015])
            cfg["hydra_args"]["agent.algorithm.num_learning_epochs"] = tune.randint(3, 10)
            cfg["hydra_args"]["agent.algorithm.num_mini_batches"] = tune.randint(2, 8)
            cfg["hydra_args"]["agent.algorithm.learning_rate"] = tune.choice([2e-3, 1.5e-3, 1.0e-3, 5.0e-4, 1.0e-4])
            cfg["hydra_args"]["agent.algorithm.gamma"] = tune.choice([0.95, 0.99, 0.999])
            cfg["hydra_args"]["agent.algorithm.lam"] = tune.choice([0.9, 0.93, 0.95, 0.97, 0.99])
            cfg["hydra_args"]["agent.algorithm.desired_kl"] = tune.choice([0.01, 0.05, 0.1])
            cfg["hydra_args"]["agent.algorithm.value_loss_coef"] = tune.choice([0.5, 0.8, 1.0, 1.2, 1.5])
        super().__init__(cfg)


