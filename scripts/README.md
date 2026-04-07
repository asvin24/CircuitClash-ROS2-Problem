This folder contains the core Python scripts for your robot. 
* `server_waypoint.py`: The driver. It listens for coordinate goals and outputs motor commands.
* `client_mission.py`: The commander. It reads the mission file and sends goals to the server.

---

## The Core Libraries
If you look at the top of the files, you will see a few imports. Here is what they do:

* **`rclpy`**: The standard ROS 2 Python Client Library. This lets your Python code talk to the ROS 2 network.
* **`ActionServer` / `ActionClient`**: These handle the complex, asynchronous communication. Unlike standard topics, Actions allow a client to send a goal, receive continuous *feedback*, and get a final *result*.
* **`Twist` (`geometry_msgs.msg`)**: The standard message type for moving a robot. It contains `linear.x` (driving forward) and `angular.z` (steering).
* **`Odometry` (`nav_msgs.msg`)**: Contains the robot's current estimated position (`x`, `y`) and orientation.
* **`tf_transformations`**: Odometry orientation is delivered as a 3D "Quaternion" (x, y, z, w). This library magically converts that complex 3D math into simple Euler angles (Roll, Pitch, Yaw). We only care about **Yaw** (the 2D compass heading of the robot).

---

## The Callback Architecture
ROS 2 is event-driven. Instead of a standard `while(True)` loop, your code relies on **callback** functions that trigger automatically when a specific event happens.

### Server Callbacks
1. **`odom_callback(self, msg)`**
   * *Triggers:* Every time the wheels broadcast a new position (many times a second).
   * *Purpose:* To constantly update the robot's internal variables (`self.current_x`, `self.current_y`, `self.yaw`) so the brain always knows where the body is.
2. **`execute_callback(self, goal_handle)`**
   * *Triggers:* When the Client sends a new target coordinate.
   * *Purpose:* This is where your control loop lives. You will calculate the distance and angle to the target, and publish `Twist` messages until the robot arrives.

### Client Callbacks
Because Actions take a long time to complete, the Client uses asynchronous callbacks to avoid freezing the program while it waits for the robot to drive.
1. **`goal_response_callback(self, future)`**
   * *Triggers:* A split-second after sending the goal.
   * *Purpose:* Checks if the Server actually accepted the goal or rejected it.
2. **`feedback_callback(self, feedback_msg)`**
   * *Triggers:* Continuously while the robot is driving.
   * *Purpose:* Receives live updates (like distance remaining) from the server.
3. **`goal_result_callback(self, future)`**
   * *Triggers:* When the Server finally declares the goal is "Complete."
   * *Purpose:* This is where you trigger the *next* waypoint to be sent!
