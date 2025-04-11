cmake_minimum_required(VERSION 3.8)
project(rviz_publisher_example)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rviz_publisher_cmake REQUIRED)

generate_rviz_panel(
  ${CMAKE_CURRENT_SOURCE_DIR}/config/rviz_params.yaml
)

ament_package()
