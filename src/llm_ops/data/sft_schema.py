from pydantic import BaseModel, Field
from typing import List, Literal

class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str

class SFTExample(BaseModel):
    messages: List[Message]
    metadata: dict = Field(default_factory=dict)
