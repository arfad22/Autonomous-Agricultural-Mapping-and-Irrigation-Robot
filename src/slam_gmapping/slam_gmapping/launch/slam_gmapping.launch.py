#!/usr/bin/env python3
import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    config_file = os.path.join(
        get_package_share_directory('slam_gmapping'),
        'params',
        'slam_gmapping.yaml'
    )

    return LaunchDescription([
        Node(
            package='slam_gmapping',
            executable='slam_gmapping',        # <-- required in ROS 2
            name='slam_gmapping',
            output='screen',
            parameters=[config_file],
            remappings=[('/scan', '/scan')]
        ),
    ])
