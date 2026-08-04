import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction

def generate_launch_description():
    home_dir = os.path.expanduser('~')
    mediamtx_path = os.path.join(home_dir, 'mediamtx')

    # 1. Launch MediaMTX from home directory so it loads ~/mediamtx.yml
    mediamtx_node = ExecuteProcess(
        cmd=[mediamtx_path],
        cwd=home_dir,
        output='screen'
    )

    # 2. Launch pipeline with TCP transport and wallclock timestamps to prevent stream crashes
    # Zero-latency pipe: nobuffer + instant packet flushing
    pipeline_cmd = (
        "libcamera-vid -t 0 -n --inline --width 640 --height 480 --framerate 20 "
        "--bitrate 1000000 --g 20 --intra 10 --vflip --hflip -o - | "
        "ffmpeg -re -i - -c copy -f rtsp -rtsp_transport tcp -max_delay 500000 -pkt_size 1316 -flush_packets 1 rtsp://localhost:8554/test"
    )

    camera_pipeline_node = ExecuteProcess(
        cmd=[pipeline_cmd],
        shell=True,
        output='screen'
    )

    # 3. Delay the camera pipeline execution by 2 seconds so MediaMTX is fully initialized first
    delayed_camera_pipeline = TimerAction(
        period=2.0,
        actions=[camera_pipeline_node]
    )

    return LaunchDescription([
        mediamtx_node,
        delayed_camera_pipeline
    ])