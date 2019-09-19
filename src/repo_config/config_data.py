"""
To add a new configuration workflow, insert a new dictionary in the CONFIG List. Each
key/value pair is mandatory.

    {
        "config_name": "the_name_of_the_config",
        "description": "Human readable description",
        "language": ["python", "py"],  # add languages along with accepted abbreviations
        "input_str": "input to confirm if the user wants the config (yes | no)?",
        "input_validation": ["yes", "no", "y", "n"],  # validation of the user's input
        "config_format_JSON": True | False, # Bool, if true add template below.
                                            # If False, absolute path to template
        "file_config_template": {} | "/path/to/config_template.txt"
        },
        "config_destination_path": "/destination/path/filename.txt",
        "output_message": "Optional message to print after file created",
    }
If adding config for a language not listed in COMMAND_LINE_ARG_CHOICES then add to
this list
"""
import os

COMMAND_LINE_ARG_CHOICES = ["python", "py", "javascript", "js", "golang", "go"]
HOME = os.environ["HOME"]
JSON_INDENT = 2
JSON_SORT_KEYS = True
VSCODE_SETTINGS_FILE_PATH = "./.vscode/settings.json"

MANDATORY_KEYS = [
    "config_name",
    "description",
    "language",
    "input_str",
    "input_validation",
    "config_format_JSON",
    "file_config_template",
    "config_destination_path",
    "output_message",
]

CONFIG = [
    {
        "config_name": "py_formatter",
        "description": "",
        "language": ["python", "py"],
        "input_str": "black is the default. Replace with yapf formatting? (yes | no)?",
        "input_validation": ["yes", "no", "y", "n"],
        "config_format_JSON": True,
        "file_config_template": {
            "python.formatting.provider": "yapf",
            "[python]": {"editor.formatOnSave": False, "editor.formatOnPaste": True},
        },
        "config_destination_path": VSCODE_SETTINGS_FILE_PATH,
        "output_message": "",
    },
    {
        "config_name": "pyright",
        "description": "",
        "language": ["python", "py"],
        "input_str": "add pyright config (yes | no)?",
        "input_validation": ["yes", "no", "y", "n"],
        "config_format_JSON": True,
        "file_config_template": {
            "include": ["src", "test"],
            "venvPath": f"{os.getcwd()}",
            "venv": "venv",
            "pythonVersion": "3.7",
        },
        "config_destination_path": "./pyrightconfig.json",
        "output_message": "Be sure to update the settings specific to the repo",
    },
    {
        "config_name": "editorconfig",
        "description": "",
        "language": ["python", "py", "javascript", "js", "golang", "go"],
        "input_str": "add .editorconfig (yes | no)?",
        "input_validation": ["yes", "no", "y", "n"],
        "config_format_JSON": False,
        "file_config_template": f"{HOME}/code/util-scripts/src/repo_config/repo_config_templates/editorconfig.template",  # noqa E501
        "config_destination_path": ".editorconfig",
        "output_message": "Be sure to update the settings specific to the repo",
    },
    {
        "config_name": "vsc_python_dev_requirements",
        "description": "A requirements[-dev].txt of Python requirements to enhance productivity in VS Code",
        "language": ["python", "py"],
        "input_str": "add Python deps for VS Code (yes | no)?",
        "input_validation": ["yes", "no", "y", "n"],
        "config_format_JSON": False,
        "file_config_template": f"{HOME}/code/util-scripts/src/repo_config/repo_config_templates/requirements-dev.txt.template",  # noqa E501
        "config_destination_path": "./.vscode/requirements-dev.txt",
        "output_message": "Run the following as necessary:\n\n\tvirtualenv -p python3.6 venv\n\tsource venv/bin/activate\n\tpip install -r ./.vscode/requirements-dev.txt\n",  # noqa E501
    },
    {
        "config_name": "setup_cfg",
        "description": "Adds a Python setup.cfg file",
        "language": ["python", "py"],
        "input_str": "add setup.cfg? (yes | no)?",
        "input_validation": ["yes", "no", "y", "n"],
        "config_format_JSON": False,
        "file_config_template": f"{HOME}/code/util-scripts/src/repo_config/repo_config_templates/setup.cfg.template",  # noqa E501
        "config_destination_path": "setup.cfg",
        "output_message": "",
    },
    {
        "config_name": "vscode_theme_config",
        "description": "Adds theme config to VS Code",
        "language": ["javascript", "js", "golang", "go"],
        "input_str": "change theme for JS/Go dev? (yes | no)?",
        "input_validation": ["yes", "no", "y", "n"],
        "config_format_JSON": True,
        "file_config_template": {"workbench.colorTheme": "Default Dark+"},
        "config_destination_path": VSCODE_SETTINGS_FILE_PATH,
        "output_message": "",
    },
]
