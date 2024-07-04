import logging
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api import deps
from app.schemas import user as user_schemas
from app.schemas.requests_responses import RequestBody, UpdateConfig
from app.services.request_processor import AssistantProcessor
from app.services.settings import update_settings_with_config


router = APIRouter()


@router.get("/assistants_list")
async def assistants_list():
    """Роут для получения списка доступных ассистентов GPT"""

    ...



@router.patch("/settings")
async def update_settings(update_config: UpdateConfig, database: AsyncSession = Depends(deps.get_db_async)):
    return await update_settings_with_config(database, update_config)
