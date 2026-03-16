import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_ntu_robotsim = get_package_share_directory('ntu_robotsim')
    
    # Path to the explore_lite parameters
    explore_params = os.path.join(
        pkg_ntu_robotsim,
        'config',
        'explore_params.yaml'
    )

    # Include the unified launch description
    launch_unified = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ntu_robotsim, 'launch', 'unified.launch.py')
        )
    )

    # Explore Lite Node
    node_explore_lite = Node(
        package='explore_lite',
        executable='explore',
        name='explore_node',
        output='screen',
        parameters=[explore_params, {'use_sim_time': True}],
    )

    launch_explore_with_delay = TimerAction(
        period=10.0,
        actions=[node_explore_lite]
    )

    return LaunchDescription([
        launch_unified,
        launch_explore_with_delay
    ])
