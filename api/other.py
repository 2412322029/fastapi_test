from fastapi import APIRouter, BackgroundTasks

otherApp = APIRouter()


@otherApp.get("/task", summary='后台任务')
async def other_task(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}


def write_notification(email: str, message=""):
    ...
