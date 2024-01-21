from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import selectinload

from app.models.database_models import MessageThread, User, UserSettings
from app.schemas.requests_responses import Thread, ThreadUpdate
from app.services.openai_operations import ToOpenAi


async def create_message_thread(database: AsyncSession, thread: Thread, user_id: int) -> MessageThread:

    async with database as session:
        thread_id = await ToOpenAi.create_thread()
        new_thread = MessageThread(user_id=user_id, thread_id=thread_id, **thread.model_dump())
        session.add(new_thread)
        await session.commit()
        await session.refresh(new_thread)

        settings_result = await session.exec(select(UserSettings).where(UserSettings.user_id == user_id))
        settings = settings_result.first()
        settings.current_message_thread = new_thread.thread_id
        await session.commit()

        return new_thread


async def update_message_thread(database: AsyncSession, thread: ThreadUpdate):
    ...