from typing import Optional, Dict, List

from pydantic import BaseModel, config, Field, model_validator
from app.services.text_formatters import CodeBlock


class VoiceContent(BaseModel):
    mime_type: str
    content: str = Field(description="string of audio decoded with base64")


class WSProcessRequestBody(BaseModel):

    model_config = config.ConfigDict(
        arbitrary_types_allowed=True
    )

    text: Optional[str] = None
    audio: Optional[VoiceContent] = None
    additional: Optional[Dict] = Field(default_factory=dict)

    @model_validator(mode="after")
    def __validate_model(self):
        if not self.text and not self.voice:
            raise ValueError


class WSProcessResponseBody(BaseModel):

    response_text: str

    audio: Optional[str] = Field(description="string of audio decoded with base64")
    code_blocks: Optional[List[CodeBlock]] = Field(default_factory=list)



