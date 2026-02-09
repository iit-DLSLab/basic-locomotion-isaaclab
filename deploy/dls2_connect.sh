#!/bin/bash
echo "Remeber to run this file with: source dls2_connect.sh"
export ROS_DISCOVERY_SERVER=127.0.0.1:11814 && 
export ROS_SUPER_CLIENT=TRUE && 
export ROS_LOCALHOST_ONLY=0 &&
ros2 daemon stop &&
ros2 daemon start