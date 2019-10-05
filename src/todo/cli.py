"""
Todoist API integration. Run -h or --help for guidance

#################### SETUP ####################

    Store the following config as env variables
    e.g. in a .env file

    Todoist_API_Key
    PROJECT_WORK_ID
    PROJECT_ADMIN_ID
    <plus any other projects you want to import templates into>

###############################################
"""
import os

import click
import todoist

from config import FILE_CONFIG


API_KEY = os.environ["Todoist_API_Key"]
KNOWN_FILES = ["review", "ticket"]


@click.command()
@click.option("-t", "--task")
@click.option("-f", "--file")
def main(task, file):
    if task:
        todoist_quick_add(task)

    if file:
        if file not in KNOWN_FILES:
            raise click.BadParameter(
                f"Not a known file template, try one of {KNOWN_FILES}"
            )
        todoist_import_template_into_project(template_name=file)


def todoist_quick_add(task):
    api = todoist.TodoistAPI(API_KEY)
    api.sync()

    task = api.quick.add(task)

    http_code = task.get("http_code")
    if http_code:
        print(f"Error - something went wrong, code {http_code}")
    else:
        api.commit()
        print(f"Success - added task: {task}")


def todoist_import_template_into_project(template_name):
    api = todoist.TodoistAPI(API_KEY)

    config = get_file_config(template_name=template_name)
    project_id = config.get("project_id")
    filename = config.get("template_path")

    file_upload = api.templates.import_into_project(
        project_id=project_id, filename=filename
    )
    print(file_upload)


def get_file_config(template_name):
    return FILE_CONFIG[template_name]


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
