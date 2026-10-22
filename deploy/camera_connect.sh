#!/bin/bash
echo "Remember to run source ros2_localhost_connect.sh first!"
# Depth only, at 848x480 (the best depth of the D435) on /camera/camera/depth/image_rect_raw.
# run_sensor2heightmap_ros2.py decimates it to the 106x60 depth_camera of go2_env_cfg.py (decimate_depth): not the
# decimation filter of the driver, which keeps false matches. The infrared streams and the point cloud are not
# needed for the depth.
ros2 launch realsense2_camera rs_launch.py \
  enable_color:=false \
  enable_infra1:=false \
  enable_infra2:=false \
  enable_gyro:=false \
  enable_accel:=false \
  pointcloud.enable:=false \
  enable_sync:=false \
  depth_module.depth_profile:=848x480x60
