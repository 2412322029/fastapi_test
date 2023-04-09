import time, json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from jose import jwt, JWTError
from starlette import status
from websockets import InvalidMessage

import utill.monitor
from config import Config

webapp = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    @staticmethod
    async def send_personal_message(message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@webapp.websocket("/join")
async def websocket_endpoint(websocket: WebSocket, token: str):
    try:
        payload = jwt.decode(token, Config['SECRET_KEY'], algorithms=[Config['ALGORITHM']])
        print(payload)
        username: str = payload.get('sub')
        await manager.connect(websocket)
        try:
            while True:
                data = await websocket.receive_text()
                # await manager.send_personal_message(f"{data}", websocket)
                await manager.broadcast(f"{data}")
        except WebSocketDisconnect:
            manager.disconnect(websocket)
            await manager.broadcast("{'username': '服务器', 'msg': '"+username+" left' }")
        except Exception as e:
            print(e)
    except JWTError:
        raise InvalidMessage(status_code=status.WS_1008_POLICY_VIOLATION)


@webapp.websocket("/cpu")
async def cpu_webs(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            time.sleep(0.5)
            await manager.send_personal_message(json.dumps(utill.monitor.getcpumsg()), websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
