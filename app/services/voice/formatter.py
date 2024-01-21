import io
from typing import IO

from pydub import AudioSegment


class VoiceFormatter:

    @classmethod
    def ogg_bytes_to_wav(cls, ogg_bytes: bytes) -> IO[bytes]:
        segment = AudioSegment.from_file(io.BytesIO(ogg_bytes))
        buffer = io.BytesIO()
        segment.export(buffer, format="wav")
        return buffer




if __name__ == "__main__":

    from app.core.config import settings
    from pathlib import Path
    from openai import OpenAI
    client = OpenAI()

    speech_file_path = Path(__file__).parent / "speech.ogg"
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        response_format="opus",
        input="Today is a wonderful day to build something people love!"
    )

    response.write_to_file(speech_file_path)


