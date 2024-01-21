import asyncio
from typing import Union, IO, Dict, Literal

from openai import AsyncOpenAI
from openai.types.audio import Transcription

from app.core.config import settings


client = AsyncOpenAI()


class VoiceHandlerException(Exception):
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
                             ) -> Transcription:

        return await client.audio.transcriptions.create(
            model=model,
            file=speech_file,
            prompt=prompt
        )

    @classmethod
    async def text_to_speech(cls, text: str,
                             model: str = "tts-1",
                             speed: int | float = 0.85,
                             response_format: Literal["mp3", "opus", "aac", "flac"] = "opus",
                             voice: Literal["alloy", "echo", "fable", "onyx", "nova", "shimmer"] = "alloy"
                             ):
        return await client.audio.speech.create(
            input=text,
            speed=speed,
            model=model,
            response_format=response_format,
            voice=voice
        )



if __name__ == "__main__":
    res = asyncio.run(VoiceHandler.text_to_speech("Hello, how are you?"))


