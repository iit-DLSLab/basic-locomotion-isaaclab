## Installation Deploy

1. Install [pixi](https://pixi.prefix.dev/latest/installation/).

2. Activate the environment from anywhere inside the repo (it uses [pixi.toml](./pixi.toml) in the repo root). The first run creates it:

```bash
# ROS2 humble
pixi shell -e humble

# ROS2 lyrical
pixi shell -e lyrical
```

## Run Sim-to-Sim 

Choose in deploy/config.py the robot/policy you want to run. **Activate your pixi environment**. Then:

```bash
## Sim-to-Sim
python3 deploy/play_mujoco.py


## Sim-to-Sim with ROS2
source deploy/ros2_localhost_connect.sh (TERMINAL 1)
python3 deploy/run_controller_ros2.py (TERMINAL 1) 

source deploy/ros2_localhost_connect.sh (TERMINAL 2)
python3 deploy/run_simulator_ros2.py (TERMINAL 2)

source deploy/ros2_localhost_connect.sh (TERMINAL 3)
ros2 launch teleop_twist_joy teleop-launch.py joy_config:='xbox' (if want joystick) (TERMINAL 3)

```

## Run Sim-to-Real

Choose in deploy/config.py the robot/policy you want to run. **Activate your pixi environment**. This script matches well with the repo [unitree-ros2-dls](https://github.com/iit-DLSLab/unitree_ros2_dls/tree/main) that you can use to control unitree go2/b2/a2/aliengo. **If you use it, remember to source first unitree_ros2_connect.bash in every terminal.**

```bash
## Sim-to-Real with ROS2
python3 run_controller_ros2.py (TERMINAL 1)

ros2 launch teleop_twist_joy teleop-launch.py joy_config:='xbox' (if want joystick) (TERMINAL 2)
```
