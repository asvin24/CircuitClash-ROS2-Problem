#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
from waypoint_navigator.action import NavigateWaypoint
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math
# TODO: You may need to import tf_transformations to handle quaternions!

class WaypointServerNode(Node):
    def __init__(self):
        super().__init__("waypoint_server")
        self.get_logger().info("Waypoint Server Boilerplate Initialized.")
        self.cb_group = ReentrantCallbackGroup()

        # TODO: Initialize your state variables here (current_x, current_y, yaw)

        # Communication interfaces
        self.cmd_vel_pub = self.create_publisher(Twist, '/leo1/cmd_vel', 10)
        self.odom_sub = self.create_subscription(
            Odometry, '/leo1/odom', self.odom_callback, 10, callback_group=self.cb_group)
        
        self.action_server = ActionServer(
            self,
            NavigateWaypoint,
            "navigate_waypoint",
            execute_callback=self.execute_callback,
            callback_group=self.cb_group
        )

        # TODO: Define your speed limits and tolerance thresholds here

    def odom_callback(self, msg: Odometry):
        # TODO: Extract position (x, y) and orientation (yaw) from the Odometry message
        # Hint: Odometry orientation is in quaternions. You need euler angles!
        pass

    def execute_callback(self, goal_handle):
        self.get_logger().info(f"Received target: ({goal_handle.request.target_x}, {goal_handle.request.target_y})")
        
        feedback = NavigateWaypoint.Feedback()
        result = NavigateWaypoint.Result()

        control_rate = self.create_rate(20)  # 20Hz control loop

        try:
            while rclpy.ok():
                if goal_handle.is_cancel_requested:
                    goal_handle.canceled()
                    result.success = False
                    return result

                # TODO 1: Calculate the distance to the target
                # TODO 2: Calculate the angle to the target
                
                # TODO 3: Publish feedback (distance_remaining) back to the client
                
                # TODO 4: Check if the target is reached (stop condition)
                
                # TODO 5: Calculate linear and angular velocities (Build your controller here!)
                
                # TODO 6: Publish the Twist message to drive the robot

                control_rate.sleep()

        except Exception as e:
            self.get_logger().error(f"Error during execution: {e}")
            goal_handle.abort()
            result.success = False
            return result
        finally:
            # Safety stop if the loop breaks
            self.cmd_vel_pub.publish(Twist())

        return result

def main(args=None):
    rclpy.init(args=args)
    node = WaypointServerNode()
    executor = MultiThreadedExecutor(num_threads=4)
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        executor.shutdown()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()