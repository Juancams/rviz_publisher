cmake_minimum_required(VERSION 3.8)
project(rviz_publisher_cmake)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic -Werror)
endif()

find_package(ament_cmake REQUIRED)

install(DIRECTORY cmake/ scripts templates
  DESTINATION share/${PROJECT_NAME}
)

include(CMakePackageConfigHelpers)
configure_package_config_file(
  "${CMAKE_CURRENT_SOURCE_DIR}/rviz_publisher_cmakeConfig.cmake.in"
  "${CMAKE_CURRENT_BINARY_DIR}/rviz_publisher_cmakeConfig.cmake"
  INSTALL_DESTINATION share/${PROJECT_NAME}
)

install(FILES
  "${CMAKE_CURRENT_BINARY_DIR}/rviz_publisher_cmakeConfig.cmake"
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
