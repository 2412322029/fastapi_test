from fastapi import APIRouter
from api.adminapi import adminapp
from api.postapi import postapp
from api.userapi import userapp
api=APIRouter()

api.include_router(userapp, prefix='/user', tags=['用户'])
api.include_router(adminapp, prefix='/admin', tags=['管理员'])
api.include_router(postapp, prefix='/post', tags=['post'])

