import uvicorn
from fastapi import FastAPI
from uvicorn.config import LOGGING_CONFIG

from api.adminapi import adminapp
from api.postapi import postapp
from api.userapi import userapp
from config import Config
from config.log_config import my_LOGGING_CONFIG

app = FastAPI(
    title='api docs',
    version='1.0',
    description='接口文档'
)


@app.on_event("startup")
async def startup():
    ...


@app.on_event("shutdown")
async def shutdown():
    ...


app.include_router(userapp, prefix='/api/user', tags=['用户'])
app.include_router(adminapp, prefix='/api/admin', tags=['管理员'])
app.include_router(postapp, prefix='/api/post', tags=['post'])

log_cfg = my_LOGGING_CONFIG if Config['Development'] else LOGGING_CONFIG


if __name__ == '__main__':
    c = Config["uvicorn"]
    uvicorn.run(app='app:app',
                host=c["host"],
                port=c["port"],
                reload=Config['Development'],
                workers=c['workers'],
                log_config=log_cfg,
                )
