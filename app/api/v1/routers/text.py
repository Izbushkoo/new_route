import logging
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api import deps
from app.schemas import user as user_schemas
from app.schemas.requests_responses import RequestBody, ResponseBody
from app.services.request_processor import AssistantProcessor


router = APIRouter()


@router.post("/request", response_model=RequestBody)
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

