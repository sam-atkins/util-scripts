"""
Adds template config files to a repo. Run in the destination repo to add these files.

VS Code defaults are set to Black, formatOnSave True and formatOnPaste False.
A VS Code settings file can be added to override with Yapf formatting to override on
a repo specific basis

#################### SETUP ####################

    Ensure you have a HOME env variable setup

###############################################
"""
import argparse
import json
import os
import sys


from typing import List, Optional

from config_data import CONFIG, MANDATORY_KEYS

COMMAND_LINE_ARG_CHOICES = ["python", "py", "javascript", "js"]
JSON_INDENT = 2
JSON_SORT_KEYS = True


def main():
    """
    Control flow for the script
    """
    validate_config_keys()
    language = get_cli_args()
    config_list = build_config_list(language=language)
    create_repo_files(config_list=config_list)


def get_cli_args() -> str:
    """
    Setups up the available arguments that can be passed in at the command line when
    running this

    Returns:
        str: the language specified by the user running the script
    """
    parser = argparse.ArgumentParser(description="Get language repo setup")
    parser.add_argument("language", choices=COMMAND_LINE_ARG_CHOICES)
    args = parser.parse_args()
    language = args.__getattribute__("language")
    return language


def validate_config_keys():
    """
    Validates that all the dictionaries in config_date.CONFIG have the mandatory keys
    """
    for key in MANDATORY_KEYS:
        for conf in CONFIG:
            if key not in conf:
                print(f"'{key}' missing from config for '{conf['config_name']}'")
                sys.exit()


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


def get_user_input(
    input_str: Optional[str], input_validation: Optional[List[str]]
) -> str:
    """
    Gets user input via the command line through a series of questions. User responses
    are validated

    Args:
        input_str (Optional[str]): A question to the user if they want to add a config
        input_validation (Optional[List[str]]): Use to validate the user response

    Returns:
        str: the validated user response
    """
    while True:
        user_input = input(input_str + "\n")
        if user_input.lower() not in (input_validation):
            print("Invalid entry, please try again")
        else:
            return user_input


def create_repo_files(config_list: List[str]):
    """
    Iterates through config_data.CONFIG and if the config_name is in the passed in list
    writes the config file to the user's repo

    Args:
        config_list (List[str]): A list of config files the user has selected
    """
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
                    output_file_path=config_destination_path,
                    file_template=file_config,
                    output_message=output_message,
                )


def make_dir(dir_name: str):
    """
    Makes a directory if it did not previously exist

    Args:
        dir_name (str): the directory name
    """
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        print("Created empty ./.vscode folder")


def write_json_file(output_file_path: str, file_config: dict, output_message: str = ""):
    """
    Writes a JSON file to the specified output file path. The append functionality is
    basic and just appends another JSON object to the existing one, requiring manual
    fix to correct the syntax. Improving this is a TODO for another day.

    Args:
        output_file_path (str): the destination where the JSON is written
        file_config (dict): the JSON contents to be written
        output_message (str, optional): Any optional message to print to the user once
                                        the file is written. Defaults to "".
    """
    mode = "w"
    complete_message = f"👍  File {output_file_path} created. {output_message}"
    if os.path.isfile(output_file_path):
        mode = "a"
        complete_message = (
            f"👍  Added config to {output_file_path}, pls correct any issues with the "
            f"JSON file syntax. {output_message}"
        )

    with open(output_file_path, mode) as outfile:
        json.dump(file_config, outfile, indent=JSON_INDENT, sort_keys=JSON_SORT_KEYS)
    print(complete_message)


def write_file(output_file_path: str, file_template: str, output_message: str = ""):
    """
    Writes a file to the specified output file path

    Args:
        output_file_path (str): the destination where the file is written
        file_template (str): the path of the template file
        output_message (str, optional): Any optional message to print to the user once
                                        the file is written. Defaults to "".
    """
    print(f"output msg: {output_message}")
    with open(output_file_path, "w") as output_file:
        file_in = open(file_template)
        output_file.write(file_in.read())
    print(f"👍  File {output_file_path} created. {output_message}")


if __name__ == "__main__":
    main()
