#!/bin/bash
echo "Setup unitree ros2 environment"
CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
#CURRENT_DIR="$(pwd)"
echo "Current dir: $CURRENT_DIR"
source $CURRENT_DIR/unitree_ros2/cyclonedds_ws/install/setup.bash
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export ROS_DOMAIN_ID=0 # Set a unique domain ID for your local environment
export CYCLONEDDS_URI='<CycloneDDS><Domain><General><Interfaces>
                            <NetworkInterface name="enp98s0" priority="default" multicast="default" />
                        </Interfaces></General></Domain></CycloneDDS>'
