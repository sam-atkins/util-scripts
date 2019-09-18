"""
Todoist API integration. Run -h or --help for guidance

#################### SETUP ####################

    Store your Todoist_API_Key as an env variable
    e.g. in .env

###############################################
"""
import argparse
import os

import todoist


def main():
    Todoist_API_Key = os.environ["Todoist_API_Key"]
    api = todoist.TodoistAPI(Todoist_API_Key)
    api.sync()

    parser = argparse.ArgumentParser(description="Todoist CLI integration tool")
    parser.add_argument("task")
    args = parser.parse_args()
    task = api.quick.add(args.task)

    http_code = task.get("http_code")
    if http_code:
        print(f"Error - something went wrong, code {http_code}")
    else:
        api.commit()
        print(f"Success - added task: {args.task}")


if __name__ == "__main__":
    main()
