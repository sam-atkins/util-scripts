"""
Adds template config files to a repo. Run in the destination repo to add these files.

VS Code defaults are set to Black, formatOnSave True and formatOnPaste False.
A VS Code settings file can be added to override with Yapf formatting to override on
a repo specific basis

TODO(sam) refactor to make it configuration based to simplify adding/removing config
          files to a script workflow
"""
import argparse
from collections import namedtuple
import json
import os
from typing import List

PythonConfig = namedtuple(
    "python_config", ["formatter", "pyright", "editorconfig", "setup_cfg"]
)
JSConfig = namedtuple("js_config", ["theme", "editorconfig"])

EDITORCONFIG_PATH = ".editorconfig"
EDITORCONFIG_TEMPLATE_PATH = "./src/repo_config_templates/editorconfig.template"
JSON_INDENT = 2
JSON_SORT_KEYS = True
PYRIGHT_CONFIG = {
    "include": ["src", "test"],
    "venvPath": "./env/bin/python",
    "venv": "env",
    "pythonVersion": "3.6",
}
PYRIGHT_SETTINGS_FILE_PATH = "./pyrightconfig.json"
SETUP_CFG_PATH = "setup.cfg"
SETUP_CFG_TEMPLATE_PATH = "./src/repo_config_templates/setup.cfg.template"
VSCODE_JS_CONFIG = {"workbench.colorTheme": "Default Dark+"}
VSCODE_PYTHON_CONFIG = {
    "python.formatting.provider": "yapf",
    "[python]": {"editor.formatOnSave": False, "editor.formatOnPaste": True},
}
VSCODE_SETTINGS_FILE_PATH = "./.vscode/settings.json"


def get_cli_args():
    parser = argparse.ArgumentParser(description="Get language repo setup")
    parser.add_argument("language", choices=["python", "py", "javascript", "js"])
    args = parser.parse_args()
    language = args.__getattribute__("language")
    return language


def make_dir(dir_name: str):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def write_json_file(output_file_path: str, file_config: dict, output_message: str = ""):
    with open(output_file_path, "w") as outfile:
        json.dump(file_config, outfile, indent=JSON_INDENT, sort_keys=JSON_SORT_KEYS)
    print(f"👍  File {output_file_path} created. {output_message}")


def write_file(output_file_path: str, file_template: str, output_message: str = ""):
    with open(output_file_path, "w") as output_file:
        file_in = open(file_template)
        output_file.write(file_in.read())
    print(f"👍  File {output_file_path} created. {output_message}")


def get_user_input(input_str: str, input_validation: List[str]):
    while True:
        user_input = input(input_str + "\n")
        if user_input.lower() not in (input_validation):
            print("Invalid entry, please try again")
        else:
            return user_input


def confirm_js_config():
    input_validation_yes_no = ["yes", "no", "y", "n"]
    editorconfig = False
    theme = True
    editorconfig_required = get_user_input(
        input_str="add .editorconfig (yes | y | no | n)?",
        input_validation=input_validation_yes_no,
    )
    if editorconfig_required.lower() in ["yes", "y"]:
        editorconfig = True

    js_config = JSConfig(theme, editorconfig)

    return js_config


def confirm_python_config():
    input_validation_yes_no = ["yes", "no", "y", "n"]
    formatter_config = False
    pyright_config = False
    editorconfig = False
    setup_cfg = False

    formatter_required = get_user_input(
        input_str="black or yapf formatting? (black | b | yapf | y)",
        input_validation=["b", "y", "black", "yapf"],
    )
    if formatter_required.lower() in ["yapf", "y"]:
        formatter_config = True

    pyright_required = get_user_input(
        input_str="add pyright config (yes | y | no | n)?",
        input_validation=input_validation_yes_no,
    )
    if pyright_required.lower() in ["yes", "y"]:
        pyright_config = True

    editorconfig_required = get_user_input(
        input_str="add .editorconfig (yes | y | no | n)?",
        input_validation=input_validation_yes_no,
    )
    if editorconfig_required.lower() in ["yes", "y"]:
        editorconfig = True

    setup_cfg_required = get_user_input(
        input_str="add setup.cfg (yes | y | no | n)?",
        input_validation=input_validation_yes_no,
    )
    if setup_cfg_required.lower() in ["yes", "y"]:
        setup_cfg = True

    python_config = PythonConfig(
        formatter_config, pyright_config, editorconfig, setup_cfg
    )

    return python_config


def create_repo_files(language: str):
    if language.lower() in ["python", "py"]:
        python_config = confirm_python_config()
        if python_config.formatter:
            make_dir("./.vscode")
            write_json_file(
                output_file_path=VSCODE_SETTINGS_FILE_PATH,
                file_config=VSCODE_PYTHON_CONFIG,
            )
        if python_config.pyright:
            write_json_file(
                output_file_path=PYRIGHT_SETTINGS_FILE_PATH,
                file_config=PYRIGHT_CONFIG,
                output_message="Be sure to update the settings specific to the repo",
            )
        if python_config.editorconfig:
            write_file(
                output_file_path=EDITORCONFIG_PATH,
                file_template=EDITORCONFIG_TEMPLATE_PATH,
            )
        if python_config.setup_cfg:
            write_file(
                output_file_path=SETUP_CFG_PATH, file_template=SETUP_CFG_TEMPLATE_PATH
            )
    elif language.lower() in ["js", "javascript"]:
        js_config = confirm_js_config()
        if js_config.theme:
            make_dir("./.vscode")
            write_json_file(
                output_file_path=VSCODE_SETTINGS_FILE_PATH, file_config=VSCODE_JS_CONFIG
            )
        if js_config.editorconfig:
            write_file(
                output_file_path=EDITORCONFIG_PATH,
                file_template=EDITORCONFIG_TEMPLATE_PATH,
            )
    else:
        print(f"Config files not yet implemented for language {language}")


def main():
    language = get_cli_args()
    create_repo_files(language=language)


if __name__ == "__main__":
    main()
