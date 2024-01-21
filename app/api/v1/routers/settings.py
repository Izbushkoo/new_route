import logging
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api import deps
from app.schemas import user as user_schemas
from app.schemas.requests_responses import RequestBody
from app.services.request_processor import AssistantProcessor


router = APIRouter()

