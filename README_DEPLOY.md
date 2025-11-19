

### Installation Deploy

1. install [miniforge](https://github.com/conda-forge/miniforge/releases) (x86_64 or arm64 depending on your platform)

2. create an environment using the file in the folder [deploy/installation](https://github.com/iit-DLSLab/basic-locomotion-dls-isaaclab/tree/main/deploy/installation):


```bash
conda env create -f mamba_environment_ros1.yaml
conda activate basic_locomotion_dls_isaaclab_ros1_env

conda env create -f mamba_environment_ros2.yaml
conda activate basic_locomotion_dls_isaaclab_ros2_env
```


or using docker
```bash
docker build -t basic_locomotion_dls_isaaclab_image .
```

putting in your .bashrc the following alias
```bash
alias basic_locomotion_dls_isaaclab_docker='
if [ ! "$(docker ps -a -q -f name=basic_locomotion_dls_isaaclab_container)" ]; then
   xhost + && docker run -it --rm -v absolute_path_to_this_repo:/home/ -v /tmp/.X11-unix:/tmp/.X11-unix --device=/dev/input/ -e DISPLAY=$DISPLAY -e WAYLAND_DISPLAY=$WAYLAND_DISPLAY -e QT_X11_NO_MITSHM=1 --gpus all --net host --cap-add=sys_nice --name basic_locomotion_dls_isaaclab_container basic_locomotion_dls_isaaclab_image; \
else
   docker exec -it basic_locomotion_dls_isaaclab_container bash; \
fi'
```


### Run Sim-to-Sim and Sim-to-Real


```bash
## Sim-to-Sim
python3 deploy/play_mujoco.py

## Sim-to-Real with ROS1
cd deploy/ros1_ws
catkin_make install -j4
source install/setup.bash
python3 deploy/run_controller_ros1.py

## Sim-to-Real with ROS2
cd deploy/ros2_ws
colcon build
source install/setup.bash
python3 deploy/run_controller_ros2.py 
ros2 launch teleop_twist_joy teleop-launch.py joy_config:='xbox' (if want joystick)
```
