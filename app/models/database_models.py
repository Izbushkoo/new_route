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

    user_id: int = Field(primary_key=True, foreign_key="users.id")
    user: "User" = Relationship(back_populates="user_settings")

    gpt_model: str = Field(default="gpt-3.5-turbo")
    current_message_thread: Optional[str] = Field(default=None, nullable=True)
    voice_answer: bool = Field(default=False)
    voice_sound: Optional[str] = Field(default="alloy")
    audio_speed: Optional[float] = Field(default=0.85)
    current_runnable: Optional[str] = Field(default="asst_q9LJrncaiC648JMIbnp2K99b")


class MessageThread(SQLModel, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    __tablename__ = "message_threads"

    thread_id: str = Field(primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    user: "User" = Relationship(back_populates="message_threads")
    name: Optional[str] = Field(default=str(uuid.uuid4))

