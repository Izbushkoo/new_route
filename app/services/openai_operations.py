import asyncio

from openai import AsyncOpenAI

from app.core.config import settings

client = AsyncOpenAI()


class ToOpenAi:

    @classmethod
    async def create_thread(cls) -> str:
        result = await client.beta.threads.create()
        return result.id


if __name__ == "__main__":
    print(asyncio.run(ToOpenAi.create_thread()))