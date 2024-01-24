import asyncio
from typing import Union, IO, Dict

from openai import AsyncOpenAI
from openai import OpenAIError

from app.models.database_models import VoiceSound


client = AsyncOpenAI()


class VoiceHandlerException(OpenAIError):
    pass


class VoiceHandler:

    @classmethod
    def validate_size(cls, file_size: Union[int, float]):
        if file_size < 25 * (1024 * 1024):
            return True
        else:
            return False

    @classmethod
    async def speech_to_text(cls, speech_file: IO[bytes], model: str = "whisper-1", prompt: str = None
                             ) -> str:
        try:
            result = await client.audio.transcriptions.create(
                model=model,
                file=speech_file,
                prompt=prompt
            )
        except OpenAIError as e:
            raise VoiceHandlerException(f"Error encountered while getting speech transcription\n originate from {e}")
        else:
            return result.text

    @classmethod
    async def text_to_speech(cls, text: str,
                             model: str = "tts-1",
                             speed: int | float = 0.85,
                             response_format: str = "opus",
                             voice: VoiceSound | str = "alloy"
                             ) -> bytes:
        try:
            result = await client.audio.speech.create(
                input=text,
                speed=speed,
                model=model,
                response_format=response_format,
                voice=voice
            )
        except OpenAIError as e:
            raise VoiceHandlerException(f"Error encountered while getting speech transcription\n originate from {e}")
        else:
            return result.read()


