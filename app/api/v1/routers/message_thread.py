import logging
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api import deps
from app.schemas import user as user_schemas
from app.schemas.requests_responses import RequestBody, Thread, ThreadUpdate
from app.services.request_processor import AssistantProcessor
from app.services.threads import create_message_thread


router = APIRouter()


@router.post("/create")
async def create_new_chat(thread: Thread,
                          user: user_schemas.UserInDBBase = Depends(deps.get_current_user),
                          database: AsyncSession = Depends(deps.get_db_async)
                          ):
    return await create_message_thread(
        database=database,
        thread=thread,
        user_id=user.id
    )


@router.put("/update")
async def update_chat(thread: ThreadUpdate,
                      user: user_schemas.UserInDBBase = Depends(deps.get_current_user),
                      database: AsyncSession = Depends(deps.get_db_async)
                      ):
    return


