#!/usr/bin/env python3
import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # 1. Static Transform: base_link -> laser_frame
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='base_to_laser_broadcaster',
            arguments=['0', '0', '0.1', '0', '0', '0', 'base_link', 'laser_frame'],
            output='screen'
        ),

        # 2. Fake Odometry Publisher (odom -> base_link)
        Node(
            package='my_robot',
            executable='fake_odom_publisher',
            name='fake_odom_publisher',
            output='screen'
        ),
    ])
