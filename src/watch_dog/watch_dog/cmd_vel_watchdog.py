import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from rclpy.qos import QoSProfile, ReliabilityPolicy
import time


class CmdVelWatchdog(Node):
    def __init__(self):
        super().__init__('cmd_vel_watchdog')

        self.declare_parameter('timeout_sec', 0.4)
        self.timeout_sec = self.get_parameter('timeout_sec').value

        qos = QoSProfile(depth=1, reliability=ReliabilityPolicy.BEST_EFFORT)

        self.last_msg_time = time.monotonic()
        self.stopped = False  # avoids spamming zero-publishes every tick

        self.sub = self.create_subscription(
            Twist, '/cmd_vel_raw', self.cmd_vel_callback, qos)

        self.pub = self.create_publisher(Twist, '/cmd_vel', qos)

        # Check twice as often as the timeout so we react promptly
        self.timer = self.create_timer(self.timeout_sec / 2.0, self.check_timeout)

    def cmd_vel_callback(self, msg: Twist):
        self.last_msg_time = time.monotonic()
        self.stopped = False
        self.pub.publish(msg)

    def check_timeout(self):
        elapsed = time.monotonic() - self.last_msg_time
        if elapsed > self.timeout_sec and not self.stopped:
            self.get_logger().warn(
                f'No /cmd_vel_raw for {elapsed:.2f}s — stopping robot.')
            self.pub.publish(Twist())  # all zeros
            self.stopped = True


def main():
    rclpy.init()
    node = CmdVelWatchdog()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()