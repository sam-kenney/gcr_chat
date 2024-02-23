"""Test the bot client."""
from __future__ import annotations

import inspect

import pytest

from gcr_chat.chatbot.client import Bot
from gcr_chat.chatbot.command import Command
from gcr_chat.chatbot.exceptions import CommandNotFoundError


def hello(name: str, age: int = 18) -> str:  # pragma: no cover
    """Say hello."""
    return f"Hello {name}, you are {age} years old."


def test_create_bot() -> None:
    """Test that a bot can be created."""
    bot = Bot()
    assert bot.prefix == "!"
    assert len(bot.commands) == 1


def test_help_no_methods() -> None:
    """Test that the help command works with no methods."""
    bot = Bot()
    bot.commands = []
    assert bot.help_() == ""


def test_help() -> None:
    """Test that the help command works."""
    bot = Bot()
    assert bot.help_() == "!help: Display the help message.\n"


def test_help_with_additional_methods() -> None:
    """Test that the help command works with additional methods."""
    bot = Bot()
    bot.command(hello)
    assert bot.help_() == (
        "!help: Display the help message.\n\n"
        "!hello: Say hello.\n"
        "    <name: str>\n"
        "    optional(<age: int = 18>)\n"
    )


def test_lookup_command() -> None:
    """Test that a command can be looked up."""
    bot = Bot()
    bot.command(hello)
    assert bot._lookup_command(["hello"]) == (
        Command(
            name="hello",
            fn=hello,
            signature=inspect.signature(hello),
            doc="Say hello.",
        ),
        [],
    )


def test_lookup_nonexistent_command() -> None:
    """Test that an error is raised if a command does not exist."""
    bot = Bot()
    with pytest.raises(CommandNotFoundError):
        bot._lookup_command(["goodbye"])


def test_clean_command() -> None:
    """Test that a command can be cleaned."""
    assert Bot()._clean_command("!hello  world") == "hello world"
    assert Bot()._clean_command("!hello  world  ") == "hello world"
    assert Bot()._clean_command("  !hello  world  ") == "hello world"
