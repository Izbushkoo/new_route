from typing import Optional, List

from pydantic import BaseModel, config, Field
from app.services.text_formatters import CodeBlock


class RequestBody(BaseModel):
    message: str


class ResponseBody(BaseModel):
    """Атрибут 'audio' содержит закодированный в base64 аудиофайл формата, согласно пользовательским настройкам."""
    model_config = config.ConfigDict(
        arbitrary_types_allowed=True
    )
    text: str
    audio: Optional[str] = None
    code_blocks: Optional[List[CodeBlock]] = Field(default_factory=list)


class Thread(BaseModel):
    name: str


class ThreadUpdate(BaseModel):
    name: Optional[str]


class UpdateConfig(BaseModel):
    user_id: int
    name: str
    value: str | bool | None | float

