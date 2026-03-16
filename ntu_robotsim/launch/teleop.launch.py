from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='teleop_twist_keyboard',
            executable='teleop_twist_keyboard',
            name='teleop_twist_keyboard',
            output='screen',
            remappings=[
                ('/cmd_vel', '/atlas/cmd_vel')
            ],
            prefix='xterm -e'  # Run in a separate terminal if possible, otherwise this might be tricky in a headless environment
        )
    ])
