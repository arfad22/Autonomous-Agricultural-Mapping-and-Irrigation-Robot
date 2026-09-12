# Autonomous Agricultural Mapping & Irrigation Robot

[![ROS 2](https://img.shields.io/badge/ROS%202-Humble%20%7C%20Foxy-343434.svg?logo=ros&logoColor=white)](https://docs.ros.org/en/humble/)
[![Language](https://img.shields.io/badge/Language-C%2B%2B%20%7C%20Python-blue.svg)](https://www.python.org/)
[![SLAM](https://img.shields.io/badge/SLAM-GMapping%20%2F%20Cartographer-green.svg)](https://github.com/ros-perception/slam_gmapping)
[![Sensor](https://img.shields.io/badge/LiDAR-YDLIDAR%202D-orange.svg)](https://www.ydlidar.com/)
[![License](https://img.shields.io/badge/License-Apache%202.0-lightgrey.svg)](LICENSE)

An autonomous mobile robotic system designed for indoor/outdoor agricultural environments, greenhouses, and orchards. It combines 360° 2D LiDAR scanning, wheel odometry kinematics, and real-time SLAM (Simultaneous Localization and Mapping) in **ROS 2** to generate high-resolution field occupancy maps for precise navigation and targeted irrigation.

---

## Key Features

- **2D LiDAR SLAM:** Real-time occupancy grid mapping (/map) using slam_gmapping.
- **Hardware Integration:** Configured for YDLIDAR (X4 / X2 / G2) via ydlidar_ros2_driver.
- **Kinematics & Odometry:** Custom my_robot package providing /odom broadcasting and static TF transformations.
- **REP-105 Compliant TF Tree:** Fully connected coordinate frame chain (map -> odom -> ase_link -> laser_frame).
- **Control Architecture:** Differential drive control and simulation support via os2_control and TurtleBot3 modules.
- **Automated CI/CD:** GitHub Actions workflows for continuous build verification on ROS 2 Humble.

---

## TF Frame Hierarchy

`	ext
  [ map ]
     │
     ▼  (Published by SLAM / GMapping)
  [ odom ]
     │
     ▼  (Published by my_robot / Odometry)
  [ base_link ]
     │
     ▼  (Static TF Broadcaster: [0, 0, 0.1, 0, 0, 0])
  [ laser_frame ]
`

---

## Hardware & Software Stack

### Hardware
| Component | Details |
| :--- | :--- |
| **LiDAR Sensor** | YDLIDAR X4 / X2 / G2 (360° 2D LiDAR, 115200 baud, /dev/ttyUSB0) |
| **Compute Platform** | Single Board Computer (Raspberry Pi 4 / NVIDIA Jetson / Laptop) |
| **Mobile Base** | 2WD / 4WD Differential Drive Chassis |
| **Actuation** | DC Motor Drivers, Relay Module, Submersible Irrigation Pump |

### Software
- **OS:** Ubuntu 22.04 LTS (Jammy) / Ubuntu 20.04 LTS (Focal)
- **Middleware:** ROS 2 Humble Hawksbill (or Foxy)
- **Build System:** colcon with ment_cmake and ment_python
- **Visualization:** RViz2

---

## Repository Structure

`	ext
.
├── .github/
│   └── workflows/
│       ├── ci.yml                    # Automated build & test on ROS 2 Humble
│       └── deploy.yml                # Workspace source packaging & release
├── docs/
│   └── tf_tree/                      # Verified TF frame trees (.gv, .pdf)
├── src/
│   ├── my_robot/                     # Robot odometry publisher & bringup launch
│   ├── ydlidar_ros2_driver/          # YDLIDAR driver, launch files, and params
│   ├── slam_gmapping/                # GMapping SLAM package for ROS 2
│   ├── turtlebot3/                   # Robot descriptions, bringup, and teleop
│   ├── ros2_control/                 # ROS 2 hardware abstraction framework
│   └── ros2_controllers/             # Differential drive & trajectory controllers
├── workspace.repos                   # Upstream package source definitions
├── .gitignore                        # Standard ROS 2 colcon ignore rules
└── README.md                         # Project documentation
`

---

## Quickstart Guide

### 1. Prerequisites & Dependencies

Install required ROS 2 packages and build tools:

`ash
sudo apt update && sudo apt install -y \
  python3-colcon-common-extensions \
  python3-rosdep \
  python3-vcstool \
  ros--tf2-ros \
  ros--nav-msgs \
  ros--geometry-msgs \
  ros--rviz2 \
  ros--nav2-map-server
`

### 2. Build the Workspace

`ash
# Clone the repository
git clone https://github.com/arfad22/Autonomous-Agricultural-Mapping-and-Irrigation-Robot.git
cd Autonomous-Agricultural-Mapping-and-Irrigation-Robot

# Build packages
colcon build --symlink-install

# Source workspace
source install/setup.bash
`

### 3. Grant Serial Port Permissions

Ensure your user has access to the LiDAR's USB interface:

`ash
sudo chmod 666 /dev/ttyUSB0
# Or add user to the dialout group permanently:
sudo usermod -aG dialout 
`

---

## Running the System

Open separate terminal windows and source the workspace in each (source install/setup.bash):

### Terminal 1: Launch YDLIDAR Driver
Publishes 2D LaserScan measurements to /scan (rame_id: laser_frame):
`ash
ros2 launch ydlidar_ros2_driver ydlidar_launch.py
`

### Terminal 2: Broadcast Odometry & TF Frames
Broadcasts static ase_link -> laser_frame and dynamic odom -> base_link transforms:
`ash
ros2 launch my_robot bringup_slam.launch.py
`

### Terminal 3: Launch GMapping SLAM
Builds the 2D occupancy grid map (/map) in real-time:
`ash
ros2 launch slam_gmapping slam_gmapping.launch.py
`

### Terminal 4: Visualize in RViz2
`ash
rviz2 -d src/ydlidar_ros2_driver/config/ydlidar.rviz
`

### Terminal 5: Save Generated Map
When mapping is complete, export the occupancy grid files (.pgm and .yaml):
`ash
ros2 run nav2_map_server map_saver_cli -f agricultural_field_map
`

---

## Sensor Parameters

Located at src/ydlidar_ros2_driver/params/ydlidar.yaml:

`yaml
ydlidar_ros2_driver_node:
  ros__parameters:
    port: /dev/ttyUSB0
    baudrate: 115200
    frame_id: laser_frame
    sample_rate: 3
    frequency: 10.0
    range_min: 0.1
    range_max: 12.0
    isSingleChannel: true
    support_motor_dtr: true
`

---

## Troubleshooting

- **Serial Port Error (Permission denied /dev/ttyUSB0):**  
  Run sudo chmod 666 /dev/ttyUSB0 or check if the device appears under a different port (e.g., /dev/ttyUSB1) via ls /dev/ttyUSB*.
- **TF Transform Timeout in RViz:**  
  Verify that ringup_slam.launch.py is running and that the Fixed Frame in RViz is set to map or ase_link.
- **Empty Map in SLAM:**  
  Verify that /scan is receiving valid ranges: os2 topic echo /scan --once.

---

## License & Credits

- Developed for the **7th Semester Major Project** at **RNS Institute of Technology (RNSIT)**.
- Maintained by [Arfad](https://github.com/arfad22).
- Licensed under the [Apache-2.0 License](LICENSE).
