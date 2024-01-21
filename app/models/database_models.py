import datetime
import uuid
from typing import Optional, List

from pydantic.config import ConfigDict
from sqlmodel import Field, SQLModel, Relationship


class User(SQLModel, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    full_name: str
    email: str
    password: str
    is_active: bool = True
    user_settings: "UserSettings" = Relationship(back_populates="user")
    message_threads: List["MessageThread"] = Relationship(back_populates="user")


class UserSettings(SQLModel, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    __tablename__ = "user_settings"

    id: Optional[int] = Field(primary_key=True, index=True)
    user_id: int = Field(foreign_key="users.id")
    user: "User" = Relationship(back_populates="user_settings")
    gpt_model: str = Field(default="gpt-3.5-turbo-1106")
    current_message_thread: Optional[str] = Field(default=None, nullable=True)
    response_format: Optional[str] = Field(default="text")
    voice_sound: Optional[str] = Field(default="alloy")
    audio_speed: Optional[float | int] = Field(default=0.85)


class MessageThread(SQLModel, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    __tablename__ = "message_threads"

    thread_id: Optional[str] = Field(primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    user: "User" = Relationship(back_populates="message_threads")
    name: Optional[str] = Field(default=str(uuid.uuid4))

