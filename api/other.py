from fastapi import APIRouter, BackgroundTasks, Depends
from utill.middleware import ip_count, api_path_count
from api.adminapi import get_admin

otherApp = APIRouter()


@otherApp.get("/task", summary='后台任务')
async def other_task(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}


@otherApp.get("/api_ua_count", dependencies=[Depends(get_admin)])
async def count():
    return ip_count


@otherApp.get("/api_count", dependencies=[Depends(get_admin)])
async def api_count():
    return api_path_count


def write_notification(email: str, message=""):
    ...
