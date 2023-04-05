import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from fastapi.responses import RedirectResponse
from api.index import api
from config import Config
from fastapi.staticfiles import StaticFiles

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

@app.get("/")
async def index():
    return RedirectResponse(url="/index.html")


@app.get("/admin")
async def admin():
    return RedirectResponse(url="/admin/index.html")

app.include_router(api, prefix='/api')
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/", StaticFiles(directory="static/dist"), name="static")

for route in app.routes:
    if isinstance(route, APIRoute):
        route.operation_id = route.name 

if __name__ == '__main__':
    print('后台运行: nohup python3 app.py > output.log 2>&1 &\n')
    c = Config["uvicorn"]
    uvicorn.run(app='app:app',
                host=c["host"],
                port=c["port"],
                reload=Config['Development'],
                workers=c['workers'],
                )
