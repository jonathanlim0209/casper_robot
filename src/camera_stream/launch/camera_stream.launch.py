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
    pipeline_cmd = (
        "libcamera-vid -t 0 -n --inline --width 640 --height 480 --framerate 20 "
        "--bitrate 500000 --intra 15 --vflip --hflip --flush -o - | "
        "ffmpeg -fflags nobuffer -flags low_delay -use_wallclock_as_timestamps 1 -i - "
        "-c copy -b:v 500k -maxrate 500k -bufsize 500k -f rtsp -rtsp_transport tcp rtsp://localhost:8554/test"
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