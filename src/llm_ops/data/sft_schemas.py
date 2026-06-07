from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator


Role = Literal["system", "user", "assistant"]


class ChatMessage(BaseModel):
    role: Role
    content: str = Field(min_length=1)


class SFTSample(BaseModel):
    id: str = Field(min_length=3)
    domain: str = Field(min_length=2)
    difficulty: Literal["easy", "medium", "hard"]
    source: str = Field(default="manual")
    messages: list[ChatMessage] = Field(min_length=2)

    @field_validator("messages")
    @classmethod
    def validate_chat_order(cls, messages: list[ChatMessage]) -> list[ChatMessage]:
        if messages[0].role != "system":
            raise ValueError("First message must be system")

        if not any(message.role == "user" for message in messages):
            raise ValueError("At least one user message is required")

        if messages[-1].role != "assistant":
            raise ValueError("Last message must be assistant")

        return messages
