from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package="camera_stream",   # replace with your package name
            executable="camera_publisher", # replace with your executable name
            name="camera_publisher",
            output="screen",
            parameters=[{"camera_source": 0}]
        )
    ])
