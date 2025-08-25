from launch import LaunchDescription
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([
        ExecuteProcess(
            cmd=[
                'bash', '-c',
                (
                    'libcamera-vid -t 0 -n --inline -o - | '
                    'gst-launch-1.0 fdsrc fd=0 do-timestamp=true ! '
                    'h264parse ! rtph264pay config-interval=1 pt=96 ! '
                    'udpsink host=192.168.1.36 port=5000 async=false sync=false'
                )
            ],
            output='screen'
        )
    ])


