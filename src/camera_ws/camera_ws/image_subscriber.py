import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

class ImageSubscriber(Node):
    def __init__(self):
        super().__init__('image_subscriber')
        self.bridge = CvBridge()
        self.subscription = self.create_subscription(
            Image, '/camera/image_raw', self.image_callback, 10)
        self.subscription  # Prevent unused variable warning

    def image_callback(self, msg):
        try:
            # Convert NV21 (YUV420sp) to raw bytes
            yuv_image = np.frombuffer(msg.data, dtype=np.uint8)

            # Reshape into (height + height//2, width) because NV21 has Y followed by interleaved UV
            height, width = msg.height, msg.width
            yuv_image = yuv_image.reshape((height * 3 // 2, width))

            bgr_image = cv2.cvtColor(yuv_image, cv2.COLOR_YUV2BGR_NV21)

            flipped_image = cv2.flip(bgr_image,0)

            # Display the converted image
            cv2.imshow("Camera Feed", flipped_image)
            cv2.waitKey(1)
        except Exception as e:
            self.get_logger().error(f"Failed to convert NV21 image: {e}")


def main():
    rclpy.init()
    node = ImageSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
