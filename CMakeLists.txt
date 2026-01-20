cmake_minimum_required(VERSION 3.0.2)
project(intern_ros_case)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
)

catkin_package(
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)
