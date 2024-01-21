import logging
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api import deps
from app.schemas import user as user_schemas
from app.services import user as user_service

router = APIRouter()


@router.post("/test")
async def test(
        file: UploadFile,
        user: user_schemas.User = Depends(deps.get_current_user),
        db: AsyncSession = Depends(deps.get_db_async),
        ):
    from pydub import AudioSegment
    import io

    f = io.BytesIO(await file.read())
    seg = AudioSegment.from_file(f)
    buffer = io.BytesIO()
    seg.export(buffer, format="wav")

    logging.info(f"{file.size}")
    return file.content_type
