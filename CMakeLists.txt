cmake_minimum_required(VERSION 3.8)
project(waypoint_navigator)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(action_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# Generate the custom Action
rosidl_generate_interfaces(${PROJECT_NAME}
  "action/NavigateWaypoint.action"
  DEPENDENCIES action_msgs
)

# Install the Python scripts
install(PROGRAMS
  scripts/server_waypoint.py
  scripts/client_waypoint.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()