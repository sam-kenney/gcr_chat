"""Exceptions for the Bot class."""
from __future__ import annotations


class BotError(Exception):
    """Generic exception for the Bot class."""


class CommandNotFoundError(BotError):
    """Thrown when a command is not found."""


class InvalidArgumentsError(BotError):
    """Thrown when a command is called with invalid arguments."""


class ArgumentParserError(BotError):
    """Thrown when an argument parser fails to parse arguments."""
