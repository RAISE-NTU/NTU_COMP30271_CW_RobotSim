# NTU_COMP30271_CW_RobotSim
NTU COMP30271 Robot Simulation for CW using ROS 2 Humble and Gazebo Fortress

sudo apt update
sudo apt install ros-humble-nav2-bringup

source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash

cd ~/ros2_ws
colcon build --packages-select ntu_robotsim
source install/setup.bash

ros2 launch ntu_robotsim cwmaze.launch.py

ros2 launch ntu_robotsim single_robot_sim.launch.py

ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r __node:=teleop_twist_keyboard_node_atlas -r /cmd_vel:=/atlas/cmd_vel

ros2 launch ntu_robotsim unified.launch.py

# line by line

ros2 launch ntu_robotsim cwmaze.launch.py

ros2 launch ntu_robotsim single_robot_sim.launch.py

ros2 launch odom_to_tf_ros2 atlas_odom_to_tf.launch.py

ros2 run rviz2 rviz2

ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 base_link atlas/base_link

ros2 launch nav2_bringup navigation_launch.py params_file:=/home/ntu-user/ros2_ws/install/ntu_robotsim/share/ntu_robotsim/config/nav2_params.yaml use_sim_time:=true use_rviz:=false

[controller_server-1] [INFO] [1772580157.680963312] [local_costmap.local_costmap]: Timed out waiting for transform from base_link to odom to become available, tf error: Invalid frame ID "base_link" passed to canTransform argument source_frame - frame does not exist
[controller_server-1] [INFO] [1772580158.181121754] [local_costmap.local_costmap]: Timed out waiting for transform from base_link to odom to become available, tf error: Invalid frame ID "base_link" passed to canTransform argument source_frame - frame does not exist


[controller_server-1] [INFO] [1772580782.447980018] [local_costmap.local_costmap]: Timed out waiting for transform from atlas/base_link to odom to become available, tf error: Invalid frame ID "odom" passed to canTransform argument target_frame - frame does not exist
[controller_server-1] [INFO] [1772580782.945561101] [local_costmap.local_costmap]: Timed out waiting for transform from atlas/base_link to odom to become available, tf error: Invalid frame ID "odom" passed to canTransform argument target_frame - frame does not exist



