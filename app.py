import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn.config import LOGGING_CONFIG

from api.adminapi import adminapp
from api.postapi import postapp
from api.userapi import userapp
from config import Config
from config.log_config import my_LOGGING_CONFIG

app = FastAPI(
    title='api docs',
    version='1.0',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=Config['allow_origins'],
    allow_origin_regex=Config['allow_origin_regex'],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(userapp, prefix='/api/user', tags=['用户'])
app.include_router(adminapp, prefix='/api/admin', tags=['管理员'])
app.include_router(postapp, prefix='/api/post', tags=['post'])

log_cfg = LOGGING_CONFIG if Config['Development'] else my_LOGGING_CONFIG  # Development 输出到终端

if __name__ == '__main__':
    print('后台运行: nohup python3 app.py > ./log/output.log 2>&1 &\n')
    c = Config["uvicorn"]
    uvicorn.run(app='app:app',
                host=c["host"],
                port=c["port"],
                reload=Config['Development'],
                workers=c['workers'],
                # log_config=log_cfg,
                )
