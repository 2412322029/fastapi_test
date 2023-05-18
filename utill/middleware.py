import asyncio
from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.routing import Mount
from config import Config

api_path_count = {}
ip_count = {}
lock = asyncio.Lock()


class PathMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, fastAPI_app: FastAPI):
        super().__init__(app)
        global api_path_count
        self.fastAPI_app = fastAPI_app
        self.api_routes = []  # api的path
        self.mount_routes = []  # 挂载的
        for route in fastAPI_app.routes:
            if isinstance(route, APIRoute):
                route.operation_id = route.name  # 缩短生成的openapi函数名称
                self.api_routes.append(route.path[1:])
                api_path_count.update({route.path[1:]: 0})
            elif isinstance(route, Mount):
                self.mount_routes.append(route.path)
            # else:
            #     print(route)

    async def dispatch(self, request, call_next):
        global ip_count, api_path_count
        response = await call_next(request)
        if Config['Access_statistics']:
            path = str(request.url).replace(str(request.base_url), '').split('?')[0].split('#')[0]
            if path in self.api_routes:
                async with lock:
                    count = api_path_count.get(path)
                    api_path_count.update({path: count + 1})
                    ua = request.headers.get('User-Agent')
                    ip_count.update({
                        ua: (ip_count.get(ua) or 0) + 1
                    })
                    # 持久化
            if len(ip_count) > 100:
                ip_count = dict(list(ip_count)[:100])
        path = str(request.url).replace(str(request.base_url), '')
        if path.startswith('uploads/') or path.endswith(('.js', '.css', '.html', '.svg', '.png', '.jpg', '.ico')):
            response.headers.update({'Cache-Control': 'max-age=8640'})
        elif path.startswith('api/'):
            response.headers.update({'Cache-Control': 'no-cache'})
        return response
