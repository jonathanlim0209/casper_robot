from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='cv_launcher',
            executable='cv_window_node',
            name='cv_window_node',
            output='screen'
        )
    ])
