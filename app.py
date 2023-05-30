import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse, StreamingResponse
from api.index import api
from config import Config
from sql.database import engine
from utill.middleware import PathMiddleware

app = FastAPI(
    title='api docs',
    version='0.1.0',
)

app.add_middleware(
    CORSMiddleware,
    # allow_origins=Config['allow_origins'],
    allow_origin_regex=Config['allow_origin_regex'],
    allow_methods=["*"],
    allow_headers=["*"],
)  # 跨域中间件
app.add_middleware(GZipMiddleware, minimum_size=1000)  # gzip压缩中间件
app.add_middleware(PathMiddleware, fastAPI_app=app)  # 访问统计

app.include_router(api, prefix='/api')
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")  # 文件上传目录
# 同时代理静态目录 配合custom_http_exception_handler
app.mount("/", StaticFiles(directory="static/dist", html=True), name="static")


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc):
    # api/开头的请求都有正确的错误响应， 其他作回退路由返回index.html配合vue-route history模式
    path = str(request.url).replace(str(request.base_url), '')
    if path.startswith('api/'):
        # print(path)
        return JSONResponse(
            status_code=exc.status_code,
            content={'detail': str(exc.detail)})
    elif path.startswith('uploads/'):
        file_like = open('uploads/default.jpg', mode="rb")
        return StreamingResponse(file_like, media_type="image/jpg")
    else:
        html_file = open("static/dist/index.html", 'r').read()
        return HTMLResponse(html_file)


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()


def main():
    uvicorn.run(app='app:app',
                host=Config["uvicorn"]["host"],
                port=Config["uvicorn"]["port"],
                reload=Config['Development'],
                workers=int(Config["uvicorn"]['workers']),
                headers=[("server", "fastapi")],
                proxy_headers=False
                )


if __name__ == '__main__':
    main()
