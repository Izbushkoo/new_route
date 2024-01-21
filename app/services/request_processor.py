import logging
from typing import Dict

from fastapi import UploadFile

from sqlmodel.ext.asyncio.session import AsyncSession
from langchain.agents import AgentExecutor

from app.schemas.user import UserInDBBase
from app.schemas.requests_responses import ResponseBody, Thread
from app.models.database_models import UserSettings
from app.services.assistant.agent import AgentGetter
from app.services.threads import create_message_thread


class BaseProcessor:

    def __init__(self, request: str, database: AsyncSession, user: UserInDBBase):
        self.request_text = request
        self.database = database
        self.user = user
        self.user_settings = user.user_settings

    async def get_response(self) -> ResponseBody:
        """Overwrite by child"""


class AssistantProcessor(BaseProcessor):

    __default_thread_name = "Новый чат"

    async def get_response(self) -> ResponseBody:
        thread_id = self.user_settings.current_message_thread
        if not thread_id:
            new_thread = await create_message_thread(
                thread=Thread(name=self.__default_thread_name),
                database=self.database,
                user_id=self.user.id
            )
            thread_id = new_thread.thread_id
        agent = self.get_assistant_agent(user_settings=self.user_settings)
        tools = self.prepare_tools(user_settings=self.user_settings)
        executor = self.get_executor(agent=agent, tools=tools)
        inputs = {"content": self.request_text, "thread_id": thread_id}
        result = await executor.ainvoke(input=inputs)
        return await self._prepare_response(invoke_result=result)

    async def _prepare_response(self, invoke_result: Dict) -> ResponseBody:
        body = ResponseBody(
            text=invoke_result["output"]
        )
        if self.user_settings.voice_answer:
            # todo write voice
            await ...
            body.audio = ...
        return body

    @classmethod
    def prepare_tools(cls, user_settings: UserSettings):
        return []

    @classmethod
    def get_assistant_agent(cls, user_settings: UserSettings):
        return AgentGetter.from_user_settings(user_settings=user_settings)

    @classmethod
    def get_executor(cls, agent, *args, **kwargs):
        return AgentExecutor(agent=agent, **kwargs)


class RunnableProcessor(BaseProcessor):

    async def get_response(self) -> ResponseBody:
        ...



if __name__ == "__main__":
    pr = AssistantProcessor(

    )
