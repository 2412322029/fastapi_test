import uvicorn
from fastapi import FastAPI
from api.adminapi import adminapp
from api.postapi import postapp
from api.userapi import userapp
from config import Config

app = FastAPI(
    title='api docs',
    version='1.0',
    description='接口文档'
)

app.include_router(userapp, prefix='/api/user', tags=['用户'])
app.include_router(adminapp, prefix='/api/admin', tags=['管理员'])
app.include_router(postapp, prefix='/api/post', tags=['post'])

if __name__ == '__main__':
    c = Config["fastapi"]
    uvicorn.run(app='app:app',
                host=c["host"],
                port=c["port"],
                reload=c["reload"])
