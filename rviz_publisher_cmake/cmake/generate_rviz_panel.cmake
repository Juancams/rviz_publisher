macro(generate_rviz_panel yaml_file)

  set(CMAKE_INCLUDE_CURRENT_DIR ON)
  set(CMAKE_AUTOMOC ON)
  set(GENERATED_HEADER ${CMAKE_BINARY_DIR}/include/${PROJECT_NAME}/RvizPublisherPanel.hpp)
  set(GENERATED_CPP ${CMAKE_BINARY_DIR}/src/RvizPublisherPanel.cpp)
  set(GENERATED_DEPENDENCIES ${CMAKE_BINARY_DIR}/template/dependencies.cmake)
  set(GENERATED_PLUGIN_XML ${CMAKE_CURRENT_SOURCE_DIR}/plugin/plugins_description.xml)
  set(TEMPLATES_DIR ${rviz_publisher_cmake_DIR}/templates)

  file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/include/${PROJECT_NAME})
  file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/src)
  file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/template)
  file(MAKE_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/plugin)

  execute_process(
    COMMAND python3 ${rviz_publisher_cmake_DIR}/scripts/generate_rviz_panel.py
            ${yaml_file}
            ${GENERATED_HEADER} ${GENERATED_CPP} ${GENERATED_DEPENDENCIES}
            ${GENERATED_PLUGIN_XML} ${TEMPLATES_DIR}
            ${PROJECT_NAME}
  )

  set(${PROJECT_NAME}_headers_to_moc
    ${GENERATED_HEADER}
  )

  include_directories(${CMAKE_BINARY_DIR}/include)

  set(library_name ${PROJECT_NAME})

  add_library(${library_name} SHARED
    ${GENERATED_CPP}
    ${${PROJECT_NAME}_headers_to_moc}
  )

  add_custom_target(generate_rviz_panel ALL
    DEPENDS ${GENERATED_HEADER} ${GENERATED_CPP} ${GENERATED_DEPENDENCIES}
  )

  include(${GENERATED_DEPENDENCIES})

  ament_target_dependencies(${library_name}
    ${dependencies}
  )

  target_include_directories(${library_name} PUBLIC
    ${Qt5Widgets_INCLUDE_DIRS}
    ${OGRE_INCLUDE_DIRS}
  )

  target_link_libraries(${library_name}
    rviz_common::rviz_common
    yaml-cpp
  )

  target_compile_definitions(${library_name} PRIVATE "RVIZ_DEFAULT_PLUGINS_BUILDING_LIBRARY")

  pluginlib_export_plugin_description_file(rviz_common plugin/plugins_description.xml)

  install(
    TARGETS ${library_name}
    EXPORT ${library_name}
    ARCHIVE DESTINATION lib
    LIBRARY DESTINATION lib
    RUNTIME DESTINATION bin
    INCLUDES DESTINATION include
  )

  ament_export_targets(${library_name} HAS_LIBRARY_TARGET)
  
  endmacro()
