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
        user: user_schemas.User = Depends(deps.get_current_user),
        db: AsyncSession = Depends(deps.get_db_async),
        ):

    return user.user_settings
