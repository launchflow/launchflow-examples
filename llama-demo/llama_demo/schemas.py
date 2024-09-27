from typing import Literal

from pydantic import BaseModel


class ChatMessage(BaseModel):
    content: str
    role: Literal["system", "user", "assistant"]


class Chat(BaseModel):
    message: str
    context: list[ChatMessage]
