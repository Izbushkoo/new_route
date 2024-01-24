import io
import logging
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api import deps
from app.schemas import user as user_schemas
from app.schemas.requests_responses import ResponseBody
from app.services.voice.openai_speech import VoiceHandler


router = APIRouter()


@router.post("/upload", response_model=ResponseBody)
async def upload_audio_file(file: UploadFile,
                            database: AsyncSession = Depends(deps.get_db_async),
                            user: user_schemas.UserInDBBase = Depends(deps.get_current_user)
                            ):
    """Отправить аудио файл как запрос к текущему ассистенту."""
    if file.content_type in ("audio/flac", "video/mp4", "audio/mp4", "video/mpeg", "audio/mpeg", "audio/ogg",
                             "video/ogg", "audio/wav", "video/webm"):
        if VoiceHandler.validate_size(file_size=file.size):
            request_text = VoiceHandler.speech_to_text(
                speech_file=io.BytesIO(await file.read()),
            )
            # todo write logic

        raise HTTPException(status_code=422, detail="File size is more than 25MB.")
    raise HTTPException(status_code=422, detail=f"Unsupported MIME-TYPE {file.content_type}")

