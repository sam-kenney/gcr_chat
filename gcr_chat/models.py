"""Application models."""

from __future__ import annotations

import base64

import pydantic
from typing_extensions import Self


class Message(pydantic.BaseModel):
    """A message."""

    data: str


class PubSubChatRequest(pydantic.BaseModel):
    """Wrapper around a Google Cloud PubSub message."""

    message: Message

    def __str__(self) -> str:
        """Convert to string."""
        return base64.b64decode(self.message.data).decode("utf-8")

    @classmethod
    def from_string(cls, s: str) -> Self:
        """Generate a :class:`PubSubChatRequest` from a string."""
        data = base64.b64encode(s.encode("utf-8")).decode("utf-8")
        return cls(message=Message(data=data))
