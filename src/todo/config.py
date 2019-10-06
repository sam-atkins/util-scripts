import os

HOME = os.environ["HOME"]

PROJECT_WORK_ID = os.environ["todoist_project_work_id"]
PROJECT_ADMIN_ID = os.environ["todoist_project_admin_id"]

FILE_CONFIG = {
    "review": {
        "project_id": PROJECT_ADMIN_ID,
        "template_path": f"{HOME}/code/util-scripts/src/todo/template/weeklyReviewGTD.csv",
    },
    "ticket": {
        "project_id": PROJECT_WORK_ID,
        "template_path": f"{HOME}/code/util-scripts/src/todo/template/workDevTicket.csv",
    },
}
