from fastapi import APIRouter, BackgroundTasks
from utill.middleware import ip_count, api_path_count

otherApp = APIRouter()


@otherApp.get("/task", summary='后台任务')
async def other_task(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}


@otherApp.get("/count")
async def count():
    return ip_count.__str__()


@otherApp.get("/api_count")
async def api_count():
    return api_path_count


def write_notification(email: str, message=""):
    ...
