"""
Adds template config files to a repo. Run in the destination repo to add these files.

VS Code defaults are set to Black, formatOnSave True and formatOnPaste False.
A VS Code settings file can be added to override with Yapf formatting to override on
a repo specific basis
"""
import argparse
from collections import namedtuple
import json
import os

PythonConfig = namedtuple("python_config", ["formatter", "pyright"])


JSON_INDENT = 2
JSON_SORT_KEYS = True
PYRIGHT_CONFIG = {
    "include": ["src", "test"],
    "venvPath": "./env/bin/python",
    "venv": "env",
    "pythonVersion": "3.6",
}
PYRIGHT_SETTINGS_FILE_PATH = "./pyrightconfig.json"
VSCODE_PYTHON_CONFIG = {
    "python.formatting.provider": "yapf",
    "[python]": {"editor.formatOnSave": False, "editor.formatOnPaste": True}
}
VSCODE_SETTINGS_FILE_PATH = "./.vscode/settings.json"
# TODO(sam) add templates
# setup.cfg template
# .editorconfig


def get_cli_args():
    parser = argparse.ArgumentParser(description="Get language repo setup")
    parser.add_argument("language", choices=["python", "js"])
    args = parser.parse_args()
    language = args.__getattribute__("language")
    return language


def make_dir(dir_name: str):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def write_json_file(output_file_path: str, file_config: dict, output_message: str = ""):
    with open(output_file_path, "w") as outfile:
        json.dump(file_config, outfile, indent=JSON_INDENT, sort_keys=JSON_SORT_KEYS)
    print(f"👍 File {output_file_path} created. {output_message}")


def confirm_python_config():
    formatter_config = False
    pyright_config = False
    invalid_entry_message = "Invalid entry, please try again"

    while True:
        formatter_input = input("black or yapf formatting? (black | b | yapf | y) \n")
        if formatter_input.lower() not in ("b", "y", "black", "yapf"):
            print(invalid_entry_message)
        else:
            break
    while True:
        pyright_input = input("add pyright config (yes | y | no | n)? \n")
        if pyright_input.lower() not in ("yes", "no", "y", "n"):
            print(invalid_entry_message)
        else:
            break

    if formatter_input.lower() in ("yapf", "y"):
        formatter_config = True
    if pyright_input.lower() in ("yes", "no"):
        pyright_config = True

    python_config = PythonConfig(formatter_config, pyright_config)

    return python_config


def create_repo_files(language: str):
    if language == "python":
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
    else:
        print(f"Config files not yet implemented for language {language}")


def main():
    language = get_cli_args()
    create_repo_files(language=language)


if __name__ == "__main__":
    main()
