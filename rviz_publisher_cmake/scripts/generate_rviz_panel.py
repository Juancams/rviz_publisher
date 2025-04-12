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

def generate_message_setters(msg_dict, prefix="msg"):
    code_lines = []

    def recurse(d, path):
        for k, v in d.items():
            full_path = f"{path}.{k}"
            if isinstance(v, dict):
                recurse(v, full_path)
            else:
                if isinstance(v, str):
                    value = f'"{v}"'
                elif isinstance(v, bool):
                    value = "true" if v else "false"
                else:
                    value = str(v)
                code_lines.append(f"{full_path} = {value};")

    recurse(msg_dict, prefix)
    return "\n    ".join(code_lines)

def generate_code(yaml_file, header_out, cpp_out, dependencies_out, xml_out, templates_dir, project_name):
    header_template = read_template(os.path.join(templates_dir, "panel.hpp.j2"))
    cpp_template = read_template(os.path.join(templates_dir, "panel.cpp.j2"))
    deps_template = read_template(os.path.join(templates_dir, "dependencies.cmake.j2"))
    xml_template = read_template(os.path.join(templates_dir, "plugins_description.xml.j2"))

    with open(yaml_file, "r") as f:
        data = yaml.safe_load(f)

    panels = data.get("panel", [])

    message_types = set()
    includes = ""
    find_dependencies = ""
    dependencies = ""
    pub_declarations = ""
    button_declarations = ""
    pub_initializations = ""
    button_initializations = ""

    for pub in panels:
        name_raw = pub["name"]
        name = name_raw.lower().replace(" ", "_")
        topic = pub["topic"]
        msg_type = pub["topic_type"].replace("/", "::")
        header_type = pub["topic_type"]
        message_types.add(header_type)

        pub_declarations += f'  rclcpp::Publisher<{msg_type}>::SharedPtr {name}_pub_;\n'
        button_declarations += f'  QPushButton * {name}_button;\n'

        pub_initializations += f'  {name}_pub_ = node_->create_publisher<{msg_type}>("{topic}", 10);\n'
        pub_initializations += f'  publishers_["{topic}"] = {name}_pub_;\n'

        button_initializations += f'  {name}_button = new QPushButton("{name_raw}");\n'
        button_initializations += f'  layout_->addWidget({name}_button);\n'
        button_initializations += f'  connect({name}_button, &QPushButton::clicked, this, [this]() {{\n'

        if "message" in pub:
            msg_code = f'    {msg_type} msg;\n'
            msg_code += f'    {generate_message_setters(pub["message"])}\n'
            msg_code += f'    {name}_pub_->publish(msg);\n'
        else:
            msg_code = f'    {name}_pub_->publish({msg_type}());\n'

        button_initializations += msg_code
        button_initializations += f'  }});\n'

        find_dependencies += f'find_package({msg_type.split("::")[0]} REQUIRED)\n'
        dependencies += f'{msg_type.split("::")[0]}\n'

    for msg in message_types:
        includes += f'#include <{get_message_header_from_type(msg)}>\n'

    os.makedirs(os.path.dirname(header_out), exist_ok=True)
    os.makedirs(os.path.dirname(cpp_out), exist_ok=True)
    os.makedirs(os.path.dirname(dependencies_out), exist_ok=True)

    with open(header_out, "w") as hpp:
        hpp.write(header_template.format(
            message_includes=includes,
            publisher_declarations=pub_declarations,
            button_declarations=button_declarations,
            project_name=project_name
        ))

    with open(cpp_out, "w") as cpp:
        cpp.write(cpp_template.format(
            publisher_initializations=pub_initializations,
            buttons_initializations=button_initializations,
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
