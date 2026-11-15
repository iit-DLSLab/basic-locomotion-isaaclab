## Overview

These script integrate with moe-rsl-rl to train a policy with Mixture-of-Experts (state decomposition) and/or one critic network per reward group (reward decomposition, multi-critic).

## Installation

Install [moe-rsl-rl](https://github.com/iit-DLSLab/moe-rsl-rl) in the Isaac Lab environment:

```bash
pip install -e <path-to>/moe-rsl-rl --no-deps
```

## How to use the state / reward decomposition

- Everything is configured in [moe_cfg.py](./../../source/basic_locomotion_isaaclab/basic_locomotion_isaaclab/tasks/locomotion/agents/moe_cfg.py). `decomposition` selects what is used, and the other sub-cfg is ignored:
  - `"state"`: mixture of experts, configured in `state_decomposition_cfg` (the experts split the states)
  - `"reward"`: one critic per group of reward terms, configured in `reward_decomposition_cfg` (default: one critic for the feet rewards and one for everything else)
  - `"state+reward"`: both, every critic of the reward decomposition is a mixture of experts

```python
moe_cfg = MoECfg(
    decomposition = "reward",
    state_decomposition_cfg = StateDecompositionCfg(...),
    reward_decomposition_cfg = RewardDecompositionCfg(
        groups = {
            "feet": RewardGroupCfg(terms=["feet_*", "*_contact_suggestion"]),
            "rest": RewardGroupCfg(terms=["*"]),
        },
        normalize_advantages = False,
    ),
)
```

- `terms` are fnmatch patterns of the reward terms (the keys of the `rewards` dict in `LocomotionEnv._get_rewards`): each term goes to the first group with a matching pattern, so `"*"` takes the remaining ones and must be the last group. The mapping is printed at the first step. `weight` (default 1.0) is the weight of the group's advantage in the actor loss

- Check this [how to](https://github.com/iit-DLSLab/moe-rsl-rl/blob/main/README_how_to.md) first!!!

- Train with

```bash
python scripts/moe_rsl_rl/train_moe.py --task=Locomotion-Go2-Flat --num_envs=4096
python scripts/moe_rsl_rl/train_moe.py --task=Locomotion-Go2-Rough-Blind --num_envs=4096
python scripts/moe_rsl_rl/train_moe.py --task=Locomotion-Go2-Rough-Vision --num_envs=4096
```

- Play with (it also exports `policy.pt` and `policy.onnx` in the `exported` folder of the run)

```bash
python scripts/moe_rsl_rl/play_moe.py --task=Locomotion-Go2-Flat --num_envs=16 --visualizer newton
python scripts/moe_rsl_rl/play_moe.py --task=Locomotion-Go2-Rough-Blind --num_envs=16 --visualizer newton
python scripts/moe_rsl_rl/play_moe.py --task=Locomotion-Go2-Rough-Vision --num_envs=16 --visualizer newton
```
