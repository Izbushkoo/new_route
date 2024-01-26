import base64
from typing import Dict, IO

from langchain.agents.openai_assistant import OpenAIAssistantRunnable
from sqlmodel.ext.asyncio.session import AsyncSession
from langchain.agents import AgentExecutor

from app.schemas.user import UserInDBBase
from app.schemas.requests_responses import ResponseBody, Thread
from app.models.database_models import UserSettings
from app.services.threads import create_message_thread
from app.services.voice.openai_speech import VoiceHandler
from app.services.assistant.tools import available_tools
from app.services.text_formatters import CodeExtractor


class BaseProcessor:

    def __init__(self, request: str, database: AsyncSession, user: UserInDBBase):
        self.request_text = request
        self.database = database
        self.user: UserInDBBase = user
        self.user_settings: UserSettings = user.user_settings

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

        agent = self.__get_assistant_agent_from_settings()
        tools = self.__prepare_tools()
        executor = self.get_executor(agent=agent, tools=tools)

        inputs = {"content": self.request_text, "thread_id": thread_id}
        result = await executor.ainvoke(input=inputs)

        return await self._prepare_response(invoke_result=result)

    async def _prepare_response(self, invoke_result: Dict) -> ResponseBody:

        response_text = invoke_result["output"]

        if self.user_settings.voice_answer:
            text, code_blocks = CodeExtractor.extract(response_text)
            voice = await VoiceHandler.text_to_speech(
                text=text,
                speed=self.user_settings.audio_speed,
                voice=self.user_settings.voice_sound
            )
            body = ResponseBody(
                text=text,
                code_blocks=code_blocks,
                audio=base64.b64encode(voice)
            )
            return body

        return ResponseBody(text=response_text)

    def __prepare_tools(self):
        tools = [available_tools.get(tool.name) for tool in self.user_settings.tools]
        return tools if any(tools) else []

    def __get_assistant_agent_from_settings(self):
        assistant = OpenAIAssistantRunnable(
            assistant_id=self.user_settings.current_assistant,
            model=self.user_settings.gpt_model,
            as_agent=True
        )
        return assistant

    @classmethod
    def get_executor(cls, agent, **kwargs):
        return AgentExecutor(agent=agent, **kwargs)


class RunnableProcessor(BaseProcessor):

    async def get_response(self) -> ResponseBody:
        ...



