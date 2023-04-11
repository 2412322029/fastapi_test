import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.routing import Route
from starlette.staticfiles import StaticFiles

from api.index import api
from config import Config

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
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.include_router(api, prefix='/api')


for route in app.routes:
    if isinstance(route, APIRoute):
        route.operation_id = route.name

if __name__ == '__main__':
    c = Config["uvicorn"]
    uvicorn.run(app='app:app',
                host=c["host"],
                port=c["port"],
                reload=Config['Development'],
                workers=c['workers'],
                proxy_headers=False
                )
