## Overview

These script integrate with amp-rsl-rl to train a policy with AMP.

## Installation

Install [amp-rsl-rl](https://github.com/gbionics/amp-rsl-rl) in the Isaac Lab environment:

```bash
pip install -e <path-to>/amp-rsl-rl --no-deps
```

## How to use AMP

- To train with AMP, modify the related [amp_cfg.py](./../../source/basic_locomotion_isaaclab/basic_locomotion_isaaclab/tasks/locomotion/agents/amp_cfg.py) (dataset folder, datasets and their weights, joint names, discriminator)

```bash
python scripts/amp_rl/train_amp.py --task=Locomotion-Aliengo-Flat --num_envs=4096
python scripts/amp_rl/train_amp.py --task=Locomotion-Aliengo-Rough-Blind --num_envs=4096
python scripts/amp_rl/train_amp.py --task=Locomotion-Aliengo-Rough-Vision --num_envs=4096
```

- To play a trained policy (it also exports `policy.pt` and `policy.onnx` in the `exported` folder of the run)

```bash
python scripts/amp_rl/play_amp.py --task=Locomotion-Aliengo-Flat --num_envs=16 --load_run=<run_folder> --checkpoint=model_<iteration>.pt --visualizer newton
```

## Replay the AMP dataset

To check a motion dataset, you can replay it kinematically on the robot (no policy, no physics). The dataset is loaded from the `amp_data_path` set in [amp_cfg.py](./../../source/basic_locomotion_isaaclab/basic_locomotion_isaaclab/tasks/locomotion/agents/amp_cfg.py), and `--dataset` is the name of the `.npy` file (`flat`, `boxes`, `stairs`)

```bash
python scripts/amp_rl/replay_amp_dataset.py --task=Locomotion-Aliengo-Flat --dataset=flat --visualizer newton
```

The motions in [amp_dataset](./amp_dataset) are recorded on Aliengo. The terrain is not replayed, so `boxes` and `stairs` motions will float or intersect the ground of the task.
