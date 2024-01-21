from typing import Optional

from pydantic import BaseModel


class RequestBody(BaseModel):
    message: str


class ResponseBody(BaseModel):
    """Атрибут 'audio' содержит закодированный в base64 аудиофайл формата согласно пользовательским настройкам."""
    text: str
    audio: Optional[str] = None


class Thread(BaseModel):
    name: str


class ThreadUpdate(BaseModel):
    name: Optional[str]


