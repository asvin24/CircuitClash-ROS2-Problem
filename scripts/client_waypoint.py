#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle
from rclpy.executors import MultiThreadedExecutor
from waypoint_navigator.action import NavigateWaypoint

class MissionClientNode(Node):
    def __init__(self):
        super().__init__("mission_client")
        self.get_logger().info("Mission Client Boilerplate Initialized.")
        self.action_client = ActionClient(self, NavigateWaypoint, "navigate_waypoint")
        
        # TODO: Load your coordinates from coordinates.txt or define them here

    def start_mission(self):
        self.get_logger().info("Waiting for Action Server...")
        if not self.action_client.wait_for_server(timeout_sec=5.0):
            self.get_logger().error("Action server not available. Aborting.")
            return
            
        self.get_logger().info("Server found! Starting mission.")
        # TODO: Trigger the first waypoint to be sent
        self.send_next_waypoint()

    def send_next_waypoint(self):
        # TODO: Get the next X, Y coordinate from your list

        goal_msg = NavigateWaypoint.Goal()
        # goal_msg.target_x = ...
        # goal_msg.target_y = ...

        # future = self.action_client.send_goal_async(
        #     goal_msg, feedback_callback=self.feedback_callback
        # )
        # future.add_done_callback(self.goal_response_callback)
        pass

    def feedback_callback(self, feedback_msg):
        # TODO: Extract the distance remaining from the feedback message and print it
        pass

    def goal_response_callback(self, future):
        goal_handle: ClientGoalHandle = future.result()
        if not goal_handle or not goal_handle.accepted:
            self.get_logger().warn("Goal rejected by server.")
            return

        self.get_logger().info("Goal accepted by server.")
        self._result_future = goal_handle.get_result_async()
        self._result_future.add_done_callback(self.goal_result_callback)

    def goal_result_callback(self, future):
        result = future.result().result
        if getattr(result, "success", False):
            self.get_logger().info("Waypoint reached successfully!")
            # TODO: Trigger the next waypoint to be sent 
        else:
            self.get_logger().warn("Goal failed.")
            # TODO: Handle retry logic if desired

def main(args=None):
    rclpy.init(args=args)
    
    node = MissionClientNode()
    executor = MultiThreadedExecutor(num_threads=2)
    executor.add_node(node)
    
    node.start_mission()
    
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