
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select


from app.schemas.requests_responses import UpdateConfig
from app.models.database_models import UserSettings


async def update_settings_with_config(database: AsyncSession, update_config: UpdateConfig):
    async with database as session:
        statement = select(UserSettings).where(UserSettings.user_id == update_config.user_id)
        result = await session.exec(statement)
        settings = result.first()
