from fastapi import APIRouter
from api.adminapi import adminapp
from api.other import otherApp
from api.postapi import postapp
from api.userapi import userapp
from api.websoketss import webapp
from api.commentapi import commentapp
api = APIRouter()

api.include_router(userapp, prefix='/user', tags=['用户'])
api.include_router(adminapp, prefix='/admin', tags=['管理员'])
api.include_router(postapp, prefix='/post', tags=['文章'])
api.include_router(commentapp, prefix='/comment', tags=['评论'])

api.include_router(webapp, prefix='/websocket', tags=['websocket'])
api.include_router(otherApp, prefix='/other', tags=['其他'])


