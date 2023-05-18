import datetime

from fastapi import APIRouter, BackgroundTasks, Depends
from starlette.responses import StreamingResponse

from config.options import sql_tool
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


@otherApp.get("/download_excel", dependencies=[Depends(get_admin)])
async def download_excel():
    try:
        filename = 'export-' + datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S')
        return StreamingResponse(sql_tool.to_excel(),
                                 headers={
                                     "Content-Disposition": f"attachment;filename={filename}",
                                     "Access-Control-Expose-Headers": "Content-Disposition"
                                 },
                                 media_type='application/vnd.ms-excel')
    except Exception as e:
        return e


def write_notification(email: str, message=""):
    ...
