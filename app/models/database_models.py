import uuid
from enum import Enum
from typing import Optional, List

from pydantic.config import ConfigDict
from sqlmodel import Field, SQLModel, Relationship


class VoiceSound(Enum):
    alloy = "alloy"
    echo = "echo"
    fable = "fable"
    onyx = "onyx"
    nova = "nova"
    shimmer = "shimmer"


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


class UserSettingsToolsLink(SQLModel, table=True):
    user_settings_id: int = Field(foreign_key="user_settings.user_id", primary_key=True)
    tool_id: int = Field(foreign_key="tools.id", primary_key=True)


class UserSettings(SQLModel, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True, use_enum_values=True)
    __tablename__ = "user_settings"

    user_id: int = Field(primary_key=True, foreign_key="users.id")
    user: "User" = Relationship(back_populates="user_settings")

    # Audio settings
    voice_answer: bool = Field(default=False)
    voice_sound: Optional[VoiceSound] = Field(default="alloy")
    audio_speed: Optional[float] = Field(default=0.85)  # From 0.25 to 4.0

    # Assistant settings
    current_assistant: Optional[str] = Field(default="asst_SziteqdkuV6ghYQNlmTSeeAy")
    gpt_model: str = Field(default="gpt-3.5-turbo")
    current_message_thread: Optional[str] = Field(default=None, nullable=True)

    tools: List["Tool"] = Relationship(back_populates="user_settings", link_model=UserSettingsToolsLink)

    # Runnable settings


class Tool(SQLModel, table=True):

    model_config = ConfigDict(arbitrary_types_allowed=True)
    __tablename__ = "tools"

    id: Optional[int] = Field(primary_key=True, index=True)
    name: str = Field(description="Name of the tool.")
    description: str = Field(description="Description of the tool.")

    user_settings: List["UserSettings"] = Relationship(back_populates="tools", link_model=UserSettingsToolsLink)


class MessageThread(SQLModel, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    __tablename__ = "message_threads"

    thread_id: str = Field(primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    user: "User" = Relationship(back_populates="message_threads")
    name: Optional[str] = Field(default=str(uuid.uuid4()))


