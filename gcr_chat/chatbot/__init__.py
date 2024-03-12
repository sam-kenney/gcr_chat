"""Bot package."""

__all__ = (
    "ArgumentParserError",
    "Bot",
    "BotError",
    "CommandNotFoundError",
    "InvalidArgumentsError",
)

from gcr_chat.chatbot.client import Bot
from gcr_chat.chatbot.exceptions import (
    ArgumentParserError,
    BotError,
    CommandNotFoundError,
    InvalidArgumentsError,
)
