# Copyright (c) 2022-2025, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
import pathlib
import sys

# Allow for import of items from the ray workflow.
CUR_DIR = pathlib.Path(__file__).parent
UTIL_DIR = CUR_DIR.parent
sys.path.extend([str(UTIL_DIR), str(CUR_DIR)])
import util
import blind_cfg
from ray import tune


class LocomotionAliengoFlatTuner(blind_cfg.BlindJobCfg):
    def __init__(self, cfg: dict = {}):
        cfg = util.populate_isaac_ray_cfg_args(cfg)
        cfg["runner_args"]["--task"] = tune.choice(["Locomotion-Aliengo-Flat"])
        super().__init__(cfg, vary_env_count=True, vary_mlp_param=True, vary_algorithm_param=True, vary_networks_type=True)


class LocomotionAliengoRoughBlindTuner(blind_cfg.BlindJobCfg):
    def __init__(self, cfg: dict = {}):
        cfg = util.populate_isaac_ray_cfg_args(cfg)
        cfg["runner_args"]["--task"] = tune.choice(["Locomotion-Aliengo-Rough-Blind"])
        super().__init__(cfg, vary_env_count=True, vary_mlp_param=True, vary_algorithm_param=True, vary_networks_type=False)


class LocomotionAliengoRoughVisionTuner(blind_cfg.BlindJobCfg):
    def __init__(self, cfg: dict = {}):
        cfg = util.populate_isaac_ray_cfg_args(cfg)
        cfg["runner_args"]["--task"] = tune.choice(["Locomotion-Aliengo-Rough-Vision"])
        super().__init__(cfg, vary_env_count=True, vary_mlp_param=True, vary_algorithm_param=True, vary_networks_type=True)

class LocomotionGo2FlatTuner(blind_cfg.BlindJobCfg):
    def __init__(self, cfg: dict = {}):
        cfg = util.populate_isaac_ray_cfg_args(cfg)
        cfg["runner_args"]["--task"] = tune.choice(["Locomotion-Go2-Flat"])
        super().__init__(cfg, vary_env_count=True, vary_mlp_param=True, vary_algorithm_param=True, vary_networks_type=True)


class LocomotionGo2RoughBlindTuner(blind_cfg.BlindJobCfg):
    def __init__(self, cfg: dict = {}):
        cfg = util.populate_isaac_ray_cfg_args(cfg)
        cfg["runner_args"]["--task"] = tune.choice(["Locomotion-Go2-Rough-Blind"])
        super().__init__(cfg, vary_env_count=True, vary_mlp_param=True, vary_algorithm_param=True, vary_networks_type=False)


class LocomotionGo2RoughVisionTuner(blind_cfg.BlindJobCfg):
    def __init__(self, cfg: dict = {}):
        cfg = util.populate_isaac_ray_cfg_args(cfg)
        cfg["runner_args"]["--task"] = tune.choice(["Locomotion-Go2-Rough-Vision"])
        super().__init__(cfg, vary_env_count=True, vary_mlp_param=True, vary_algorithm_param=True, vary_networks_type=True)

