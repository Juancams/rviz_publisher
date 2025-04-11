#!/usr/bin/env python3

import yaml
import sys
import os

def read_template(template_path):
    with open(template_path, "r") as f:
        return f.read()

def get_message_header_from_type(msg_type):
    msg_type_list = list(msg_type)
    output = []
    for i in range(len(msg_type_list)):
        if msg_type_list[i].isupper():
            if msg_type_list[i - 1] != '/':
                output.append('_')
            output.append(msg_type[i].lower())
        else:
            output.append(msg_type_list[i])
    return ''.join(output) + '.hpp'

def generate_code(yaml_file, header_out, cpp_out, dependencies_out, xml_out, templates_dir, project_name):
    # Leer plantillas desde archivos
    header_template = read_template(os.path.join(templates_dir, "panel.hpp.j2"))
    cpp_template = read_template(os.path.join(templates_dir, "panel.cpp.j2"))
    deps_template = read_template(os.path.join(templates_dir, "dependencies.cmake.j2"))
    xml_template = read_template(os.path.join(templates_dir, "plugins_description.xml.j2"))

    with open(yaml_file, "r") as f:
        data = yaml.safe_load(f)

    publishers = data.get("panel", {}).get("publishers", [])

    message_types = set()
    pub_declarations = ""
    pub_initializations = ""
    includes = ""
    find_dependencies = ""
    dependencies = ""

    for pub in publishers:
        topic = pub["topic"]
        msg_type = pub["type"].replace("/", "::")
        var_name = topic.replace("/", "_").strip("_")
        message_types.add(pub["type"])

        pub_declarations += f'  rclcpp::Publisher<{msg_type}>::SharedPtr {var_name}_pub_;\n'
        pub_initializations += f'  {var_name}_pub_ = node_->create_publisher<{msg_type}>("{topic}", 10);\n'
        pub_initializations += f'  publishers_["{topic}"] = {var_name}_pub_;\n'
        find_dependencies += f'find_package({msg_type.split("::")[0]} REQUIRED)\n'
        dependencies += f'{msg_type.split("::")[0]}\n'

    for msg in message_types:
        includes += f'#include <{get_message_header_from_type(msg)}>\n'

    # Crear directorios de salida si no existen
    for path in [header_out, cpp_out, dependencies_out]:
        os.makedirs(os.path.dirname(path), exist_ok=True)

    # Escribir archivos de salida con las plantillas llenas
    with open(header_out, "w") as hpp:
        hpp.write(header_template.format(
            message_includes=includes,
            publisher_declarations=pub_declarations,
            project_name=project_name
        ))

    with open(cpp_out, "w") as cpp:
        cpp.write(cpp_template.format(
            publisher_initializations=pub_initializations,
            project_name=project_name,
        ))

    with open(dependencies_out, "w") as deps:
        deps.write(deps_template.format(
            find_dependencies=find_dependencies,
            dependencies=dependencies
        ))

    with open(xml_out, "w") as xml:
        xml.write(xml_template.format(
            project_name=project_name,
        ))

if __name__ == "__main__":
    yaml_file = sys.argv[1]
    header_out = sys.argv[2]
    cpp_out = sys.argv[3]
    dependencies_out = sys.argv[4]
    xml_out = sys.argv[5]
    templates_dir = sys.argv[6]
    project_name = sys.argv[7]

    generate_code(yaml_file, header_out, cpp_out, dependencies_out, xml_out, templates_dir, project_name)
