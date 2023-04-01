import uvicorn
from fastapi import FastAPI
from api.userapi import userapp
from config import Config

app = FastAPI(
    title='api docs',
    version='1.0',
    description='接口文档'
)

app.include_router(userapp, prefix='/user', tags=['用户'])

if __name__ == '__main__':
    c = Config["fastapi"]
    uvicorn.run(app='app:app',
                host=c["host"],
                port=c["port"],
                reload=c["reload"])
