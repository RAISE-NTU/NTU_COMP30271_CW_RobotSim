import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    pkg_ntu_robotsim = get_package_share_directory('ntu_robotsim')
    pkg_nav2_bringup = get_package_share_directory('nav2_bringup')
    pkg_odom_tf = get_package_share_directory('odom_to_tf_ros2')
    pkg_octomap_server = get_package_share_directory('octomap_server2')

    nav2_params_path = os.path.join(pkg_ntu_robotsim, 'config', 'nav2_params.yaml')

    launch_maze = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_ntu_robotsim, 'launch', 'maze.launch.py'))
    )
    launch_robot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_ntu_robotsim, 'launch', 'single_robot_sim.launch.py'))
    )

    launch_odom_tf = IncludeLaunchDescription(
        # Note: Using atlas_odom_to_tf.launch.py for namespaced odom
        PythonLaunchDescriptionSource(os.path.join(pkg_odom_tf, 'launch', 'atlas_odom_to_tf.launch.py'))
    )

    launch_octomap = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_octomap_server, 'launch', 'octomap_filtered.launch.py'))
    )

    run_rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', os.path.join(pkg_ntu_robotsim, 'config', 'single_robot.rviz')]
    )

    launch_nav2 = TimerAction(
        period=5.0,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(os.path.join(pkg_nav2_bringup, 'launch', 'navigation_launch.py')),
                launch_arguments={
                    'params_file': nav2_params_path,
                    'use_sim_time': 'true',
                    'use_rviz': 'false'
                }.items()
            )
        ]
    )

    static_map_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0', '0', '0', '0', '0', '0', 'map', 'atlas/odom']
    )

    return LaunchDescription([
        launch_maze,
        launch_robot,
        launch_odom_tf,
        launch_octomap,
        run_rviz,
        launch_nav2,
        static_map_tf
    ])
