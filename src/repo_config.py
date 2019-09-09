"""
Adds template config files to a repo. Run in the destination repo to add these files.

VS Code defaults are set to Black, formatOnSave True and formatOnPaste False.
This settings file enables overrides on a repo specific basis
"""
import argparse
import json
import os


JSON_INDENT = 2
JSON_SORT_KEYS = True
PYRIGHT_CONFIG = {
    "include": ["src", "tests"],
    "venvPath": "./env/bin/python",
    "venv": "env",
    "pythonVersion": "3.6",
}
PYRIGHT_SETTINGS_FILE_PATH = "./pyrightconfig.json"
VSCODE_PYTHON_CONFIG = {
    "python.linting.flake8Enabled": True,
    "python.linting.enabled": True,
    "python.formatting.provider": "yapf",
    "[python]": {"editor.formatOnSave": False, "editor.formatOnPaste": True},
    "python.pythonPath": "/usr/local/bin/python3.6"
}
VSCODE_SETTINGS_FILE_PATH = "./.vscode/settings.json"


def get_cli_args():
    parser = argparse.ArgumentParser(description="Get language repo setup")
    parser.add_argument("language", choices=["python", "js"])
    args = parser.parse_args()
    language = args.__getattribute__("language")
    return language


def make_dir(dir_name: str):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        return True


def write_json_file(output_file_path: str, file_config: dict, output_message: str = ""):
    with open(output_file_path, "w") as outfile:
        json.dump(file_config, outfile, indent=JSON_INDENT, sort_keys=JSON_SORT_KEYS)
    print(f"👍 File {output_file_path} created. {output_message}")


def create_repo_files(language: str):
    if language == "python":
        make_dir("./.vscode")
        write_json_file(
            output_file_path=VSCODE_SETTINGS_FILE_PATH, file_config=VSCODE_PYTHON_CONFIG
        )
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
