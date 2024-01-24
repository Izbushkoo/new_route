import logging
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, WebSocket
from fastapi.responses import FileResponse, HTMLResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api import deps
from app.schemas import user as user_schemas
from app.schemas.requests_responses import RequestBody, ResponseBody
from app.services.request_processor import AssistantProcessor


router = APIRouter()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8909/new_route/api/v1/text/");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@router.post("/request", response_model=ResponseBody)
async def send_text_request(body: RequestBody,
                            database: AsyncSession = Depends(deps.get_db_async),
                            user: user_schemas.UserInDBBase = Depends(deps.get_current_user)
                            ):

    processor = AssistantProcessor(
        request=body.message,
        user=user,
        database=database,
    )
    result = await processor.get_response()
    return result


@router.get("/")
async def get():
    return HTMLResponse(html)


@router.websocket("/socket_request")
async def set_socket_connection(socket: WebSocket, user: user_schemas.UserInDBBase = Depends(deps.get_current_user)):
    await socket.accept()
    while True:
        data = await socket.receive_json()
        logging.info(f"{data}")
        await socket.send_text("hello")



