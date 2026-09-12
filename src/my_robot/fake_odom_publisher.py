#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose, Point, Quaternion, Twist
import math
import time

class FakeOdomPublisher(Node):
    def __init__(self):
        super().__init__('fake_odom_publisher')
        self.publisher_ = self.create_publisher(Odometry, '/odom', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)  # 10Hz
        self.start_time = time.time()
        self.get_logger().info("Fake /odom publisher started")

    def timer_callback(self):
        msg = Odometry()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "odom"
        msg.child_frame_id = "base_link"

        # Simulate simple circular motion
        t = time.time() - self.start_time
        msg.pose.pose.position.x = math.cos(t) * 0.5
        msg.pose.pose.position.y = math.sin(t) * 0.5
        msg.pose.pose.orientation.z = math.sin(t / 2)
        msg.pose.pose.orientation.w = math.cos(t / 2)

        msg.twist.twist.linear.x = 0.1
        msg.twist.twist.angular.z = 0.1

        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = FakeOdomPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
