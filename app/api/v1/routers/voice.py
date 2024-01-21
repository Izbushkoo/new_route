import logging
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api import deps
from app.schemas import user as user_schemas
from app.services import user as user_service


router = APIRouter()



@router.post("/upload")
async def upload_audio_file(file: UploadFile,
                            database: AsyncSession = Depends(deps.get_db_async),
                            user: user_schemas.UserInDBBase = Depends(deps.get_current_user)
                            ):
    if file.content_type in ("audio/flac", "video/mp4", "audio/mp4", "video/mpeg", "audio/mpeg", "audio/ogg",
                             "audio/wav", "video/webm"):
        ...



