# CircuitClash: Waypoint Navigator Challenge

Welcome to the codebase for your ROS 2 hackathon challenge! This repository contains the skeleton code you need to navigate the Leo Rover autonomously using a ROS 2 Action Server and Client.

Your mission is to complete the missing logic inside the `scripts` and `action` folder so the rover can read coordinates and drive to them with precision.

---

## Warning
Before you dive into the Python scripts, take a look at two critical files in this root directory: `CMakeLists.txt` and `package.xml`. 

* **Please DO NOT modify these files.** The build system is already perfectly configured for the hackathon.
* `package.xml` is the ID card of your package. It tells ROS 2 exactly which libraries this package depends on (like `geometry_msgs` and `rclpy`). 
* `CMakeLists.txt` is the instruction manual for the compiler. It tells `colcon` exactly where to find your Python scripts and custom Action definitions so they can be installed into the system.

---

## The Build System: `colcon`
Whenever you edit code in ROS 2, you must build your workspace so the system registers the changes. 

**Standard Build:**
```bash
colcon build
```

This compiles everything from scratch. If you use this, you must re-run it every time you change a single line of Python code.

**Symlink Install:**

```bash
colcon build --symlink-install
```

We highly recommend using this! It creates a "shortcut" to your Python scripts. When using --symlink-install, you can edit your Python files, save them, and immediately run them without having to compile again (most of the time).

Never forget: Always run:

```bash
source install/setup.bash
```

in any new terminal before running your nodes!

ROS 2 Survival Cheat Sheet

Debugging is half of robotics! Use these terminal commands to see what is happening under the hood while your code runs.

1. List all active topics:

```bash
ros2 topic list
```

2. Spy on the data flowing through a topic: (Great for checking if odometry is working!)

```bash
    ros2 topic echo /leo1/odom
```

3. List all active actions:

```bash
ros2 action list
```

4. See the Matrix (Visual Node Graph):

```bash
rqt_graph
```

# ALL THE BEST GANG!!
