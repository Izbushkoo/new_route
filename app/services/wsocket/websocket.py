import asyncio
import logging

from fastapi import WebSocket, WebSocketDisconnect, WebSocketException

from app.schemas.user import UserInDBBase
from app.services.wsocket.schemas import *


class SocketProcessor:

    def __init__(self,
                 websocket: WebSocket,
                 # stop: asyncio.Event,
                 # user: UserInDBBase
                 ):
        self.socket = websocket
        self.stop = asyncio.Event()
        # self.user = user
        # self.settings = user.user_settings

    def check_stop_event(self):
        if self.stop.is_set():
            ...

    async def process_connection(self):
        while True:
            try:
                data = await self.socket.receive_text()
                logging.info(f"{data}")
            except WebSocketDisconnect:
                await self.socket.close()






