#!/bin/bash
echo "Remember to run this file with: source dls2_connect.sh"
export ROS_DISCOVERY_SERVER="192.168.88.250:11812;192.168.88.250:11813;192.168.88.250:11814;192.168.88.250:11818"
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
export ROS_SUPER_CLIENT=TRUE
export ROS_LOCALHOST_ONLY=0

# Restart the ros2 CLI daemon so it picks up the settings above. A daemon left
# over from another profile (e.g. cyclone bound to an interface that went down)
# can stop answering, and `ros2 daemon stop` then waits on it forever.
timeout -k 2 5 ros2 daemon stop || {
    echo "ros2 daemon not responding, killing it"
    pkill -KILL -f "ros2cli\.daemon\.daemonize .*--ros-domain-id ${ROS_DOMAIN_ID:-0} "
    sleep 1
}
ros2 daemon start
