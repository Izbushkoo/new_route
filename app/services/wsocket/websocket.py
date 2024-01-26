import asyncio
import base64
import logging
from typing import Dict, Type, Awaitable

from fastapi import WebSocket, WebSocketDisconnect, WebSocketException

from app.schemas.requests_responses import ResponseBody
from app.schemas.user import UserInDBBase
from app.services.text_formatters import CodeExtractor
from app.services.voice.openai_speech import VoiceHandler
from app.services.wsocket.schemas import WSProcessResponseBody, WSProcessRequestBody
from app.services.wsocket.errors import BaseError, BadRequestModel, TaskRunning, TaskAborted
from app.services.request_processor import AssistantProcessor


class SocketProcessor(AssistantProcessor):

    def __init__(self,
                 websocket: WebSocket,
                 # user: UserInDBBase
                 **kwargs
                 ):
        self.socket = websocket
        self.current_task = None
        super().__init__(**kwargs)
        # self.user = user
        # self.settings = user.user_settings

    async def _prepare_response(self, invoke_result: Dict) -> WSProcessResponseBody:

        response_text = invoke_result["output"]

        if self.user_settings.voice_answer:
            text, code_blocks = CodeExtractor.extract(response_text)
            voice = await VoiceHandler.text_to_speech(
                text=text,
                speed=self.user_settings.audio_speed,
                voice=self.user_settings.voice_sound
            )
            body = WSProcessResponseBody(
                text=text,
                audio=base64.b64encode(voice),
                code_blocks=code_blocks
            )
            return body
        return WSProcessResponseBody(text=response_text)

    def check_stop_event(self, data: Dict) -> bool:
        stop = data.get("stop", False)
        if stop:
            return self.current_task.cancel()
        return False

    async def set_task(self, coro: Awaitable) -> bool:
        if self.current_task is None or self.current_task.done():
            self.current_task = asyncio.create_task(
                coro
            )
            return True
        else:
            await self.send_error(
                error=TaskRunning()
            )
            return False

    async def process_connection(self):
        while True:
            try:
                data = await self.socket.receive_json()
                logging.info(f"{data}")
                if self.check_stop_event(data):
                    await self.send_error(TaskAborted())
                else:
                    request_model = self.convert_to_request_model(data=data)

                    # todo logic with handling request
            except WebSocketDisconnect:
                await self.socket.close()

    async def convert_to_request_model(self, data: Dict):
        try:
            request_model = WSProcessRequestBody(**data)
        except ValueError:
            await self.send_error(
                error=BadRequestModel()
            )
        else:
            return request_model

    async def send_error(self, error: BaseError):
        await self.socket.send_json(
            error.model_dump()
        )





