#!/bin/bash
echo "Remember to run source ros2_localhost_connect.sh first!"
ros2 launch realsense2_camera rs_launch.py \
  enable_color:=false \
  enable_infra1:=false \
  enable_infra2:=false \
  enable_gyro:=false \
  enable_accel:=false \
  enable_pointcloud:=false \
  enable_sync:=false