import rclpy
from rclpy.node import Node
import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

mouse_x, mouse_y = 0, 0

def mouse_event(event, x, y, flags, param):
    global mouse_x, mouse_y
    if event == cv2.EVENT_MOUSEMOVE:
        mouse_x, mouse_y = x, y
        print("Mouse moved to:", x, y)

class CVWindowNode(Node):
    def __init__(self):
        super().__init__('cv_window_node')
        self.latest_img = None
        self.bridge = CvBridge()

        self.image_sub = self.create_subscription(
            Image,
            "/camera/image_raw",
            self.callback,
            rclpy.qos.QoSPresetProfiles.SENSOR_DATA.value
        )
        cv2.namedWindow("Tuning", cv2.WINDOW_NORMAL)
        cv2.setMouseCallback("Tuning", mouse_event)
        cv2.waitKey(1)

    def callback(self, msg: Image):
        """Receive image messages and store latest frame."""
        try:
            self.latest_img = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except Exception as e:
            self.get_logger().error(f"Failed to convert image: {e}")

    def spin_gui(self):

        while rclpy.ok():
            rclpy.spin_once(self, timeout_sec=0.1)

            if self.latest_img is not None:
                img = self.latest_img.copy()
            else:
                img = np.zeros((480, 640, 3), np.uint8)
            if mouse_x >= 0 and mouse_y >= 0:
                cv2.putText(img, f"Mouse: ({mouse_x}, {mouse_y})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.imshow("Tuning", img)
            if cv2.waitKey(10) & 0xFF == 27:  # ESC to exit
                break
        cv2.destroyAllWindows()

def main(args=None):
    rclpy.init(args=args)
    node = CVWindowNode()
    node.spin_gui()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
