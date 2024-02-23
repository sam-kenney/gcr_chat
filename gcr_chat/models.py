"""Application models."""
from __future__ import annotations

import base64

import pydantic


class Message(pydantic.BaseModel):
    """A message."""

    data: str


class PubSubChatRequest(pydantic.BaseModel):
    """Wrapper around a Google Cloud PubSub message."""

    message: Message

    def __str__(self) -> str:
        """Convert to string."""
        return base64.b64decode(self.message.data).decode("utf-8")
