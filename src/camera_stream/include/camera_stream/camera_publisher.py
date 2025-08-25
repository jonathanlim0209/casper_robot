import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2

class CameraPublisher(Node):
    def __init__(self):
        super().__init__('camera_publisher')
        self.publisher_ = self.create_publisher(Image, '/camera/image_raw', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)  # 10 Hz
        self.cap = cv2.VideoCapture(0)  # Change the index if necessary
        self.bridge = CvBridge()

        # declare parameter
        self.declare_parameter("camera_source", 0)
        cam_index = self.get_parameter("camera_source").value

        self.cap = cv2.VideoCapture(cam_index)  # just webcam index 0

    def timer_callback(self):
        ret, frame = self.cap.read()
        if ret:
            try:
                msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
                self.publisher_.publish(msg)
                self.get_logger().info('Publishing camera frame')
            except CvBridgeError as e:
                self.get_logger().error(f"Failed to convert image: {e}")
        else:
            self.get_logger().error("Failed to capture image from camera")


def main(args=None):
    rclpy.init(args=args)
    node = CameraPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()