# Rviz Publisher
![distro](https://img.shields.io/badge/Ubuntu%2024-Noble%20Numbat-orange) [![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![rolling](https://github.com/Juancams/rviz_publisher/actions/workflows/rolling.yaml/badge.svg)](https://github.com/Juancams/rviz_publisher/actions/workflows/rolling.yaml)

This package provides a tool to generate rviz plugins using a yaml file.

## How to use
### Build your package
In the package in which you want to generate the plugin, add the following lines to your `CMakeLists.txt`

```cmake
find_package(rviz_publisher_cmake REQUIRED)

generate_rviz_panel(
  <path_to_the_yaml>
)
```
*I'll leave you a complete example of a package that is using it [here](https://github.com/Juancams/rviz_publisher/blob/rolling/rviz_publisher_example/CMakeLists.txt).*

### View your plugin
Once built, launch Rviz2 and add a new panel. To do this, go to `Panels > Add New Panel` and then select `Rviz Publisher Panel` from your package folder. Following the example of this [yaml](https://github.com/Juancams/rviz_publisher/blob/rolling/rviz_publisher_example/config/rviz_params.yaml), it loads a configuration like this:

![image](https://github.com/user-attachments/assets/3dada19f-4171-416b-9772-d97b8a6c880d)

Now, once you click on your buttons, the information you configured in your yaml will be published.

## License

This project is licensed under the Apache License, Version 2 - see the [LICENSE](https://github.com/Juancams/rviz_publisher/blob/rolling/LICENSE) file for details.

## Author & Maintainer

* [Juan Carlos Manzanares Serrano](https://github.com/Juancams)
