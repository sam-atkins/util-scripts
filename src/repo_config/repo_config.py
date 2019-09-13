"""
Adds template config files to a repo. Run in the destination repo to add these files.

VS Code defaults are set to Black, formatOnSave True and formatOnPaste False.
A VS Code settings file can be added to override with Yapf formatting to override on
a repo specific basis

##### SETUP #####
Ensure you have a HOME env variable setup

TODO(sam)
- amend write function to append if json (./vscode/settings.json) already exists
- add fn to validate each dict is valid with CONFIG
- add flags e.g. --menu asks for options of what files to add; --pyright adds pyright
"""
import argparse
import json
import os
from typing import List, Optional

from config_data import CONFIG


JSON_INDENT = 2
JSON_SORT_KEYS = True


def main():
    # TODO(sam) validate config dict has all required keys
    language = get_cli_args()
    config_list = build_config_list(language=language)
    create_repo_files(config_list=config_list)


def get_cli_args():
    parser = argparse.ArgumentParser(description="Get language repo setup")
    parser.add_argument("language", choices=["python", "py", "javascript", "js"])
    args = parser.parse_args()
    language = args.__getattribute__("language")
    return language


def build_config_list(language: str) -> List[str]:
    """
    Builds a list of config required by the user

    Args:
        language (str): language config entered by the user as CLI arg

    Returns:
        List[str]: List of configs required e.g. ['py_formatter', 'pyright']
    """
    config_list = []
    for conf in CONFIG:
        if language in conf.get("language"):

            input_str = conf.get("input_str")
            input_validation = conf.get("input_validation")
            config_name = conf.get("config_name")

            config_required = get_user_input(
                input_str=input_str, input_validation=input_validation
            )

            if config_required.lower() in ["yes", "y"]:
                config_list.append(config_name)

    return config_list


def get_user_input(input_str: Optional[str], input_validation: Optional[List[str]]):
    while True:
        user_input = input(input_str + "\n")
        if user_input.lower() not in (input_validation):
            print("Invalid entry, please try again")
        else:
            return user_input


def create_repo_files(config_list: List[str]):
    make_dir("./.vscode")

    for conf in CONFIG:
        name = conf.get("config_name")
        if name in config_list:
            config_destination_path = conf.get("config_destination_path")
            file_config = conf.get("file_config_template")
            output_message = conf.get("output_message")

            if conf.get("config_format_JSON"):
                write_json_file(
                    output_file_path=config_destination_path,
                    file_config=file_config,
                    output_message=output_message,
                )
            else:
                write_file(
                    output_file_path=config_destination_path, file_template=file_config
                )


def make_dir(dir_name: str):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        print("Created empty ./.vscode folder")


# TODO(sam) append if JSON file already exists
def write_json_file(output_file_path: str, file_config: dict, output_message: str = ""):
    with open(output_file_path, "w") as outfile:
        json.dump(file_config, outfile, indent=JSON_INDENT, sort_keys=JSON_SORT_KEYS)
    print(f"👍  File {output_file_path} created. {output_message}")


def write_file(output_file_path: str, file_template: str, output_message: str = ""):
    with open(output_file_path, "w") as output_file:
        file_in = open(file_template)
        output_file.write(file_in.read())
    print(f"👍  File {output_file_path} created. {output_message}")


if __name__ == "__main__":
    main()
