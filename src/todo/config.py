import os

HOME = os.environ["HOME"]

PROJECT_ADMIN_ID = os.environ["todoist_project_admin_id"]
PROJECT_BUSINESS_ID = os.environ["todoist_project_business_id"]
PROJECT_PACK_LIST_ID = os.environ["todoist_project_packing_list_id"]
PROJECT_WORK_ID = os.environ["todoist_project_work_id"]

FILE_CONFIG = {
    "blog": {
        "project_id": PROJECT_BUSINESS_ID,
        "template_path": f"{HOME}/code/util-scripts/src/todo/template/blog.csv",
    },
    "pack": {
        "project_id": PROJECT_PACK_LIST_ID,
        "template_path": f"{HOME}/code/util-scripts/src/todo/template/packing_list.csv",
    },
    "review": {
        "project_id": PROJECT_ADMIN_ID,
        "template_path": f"{HOME}/code/util-scripts/src/todo/template/weeklyReviewGTD.csv",
    },
    "ticket": {
        "project_id": PROJECT_WORK_ID,
        "template_path": f"{HOME}/code/util-scripts/src/todo/template/workDevTicket.csv",
    },
}
