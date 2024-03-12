"""Test the command class."""

from __future__ import annotations

import inspect

import pytest

from gcr_chat.chatbot.client import Command
from gcr_chat.chatbot.exceptions import ArgumentParserError


def hello(name: str, age: int = 18) -> str:  # pragma: no cover
    """Say hello."""
    return f"Hello {name}, you are {age} years old."


def test_parse_args() -> None:
    """Test that arguments are parsed correctly."""
    command = Command(
        name="hello",
        fn=hello,
        signature=inspect.signature(hello),
        doc="",
    )
    args = ["John", "20"]
    assert command.parse_args(args) == ["John", 20]


def test_parse_args_missing_arg() -> None:
    """Test that an error is raised if an argument is missing."""
    command = Command(
        name="hello",
        fn=hello,
        signature=inspect.signature(hello),
        doc="",
    )
    args = ["John"]
    assert command.parse_args(args) == ["John", 18]


def test_parse_args_too_many_args() -> None:
    """Test that an error is raised if too many arguments are provided."""
    command = Command(
        name="hello",
        fn=hello,
        signature=inspect.signature(hello),
        doc="",
    )
    args = ["John", "20", "extra"]
    assert command.parse_args(args) == ["John", 20, "extra"]


def test_parse_args_too_few_args() -> None:
    """Test that an error is raised if too few arguments are provided."""
    command = Command(
        name="hello",
        fn=hello,
        signature=inspect.signature(hello),
        doc="",
    )
    args = []

    with pytest.raises(ArgumentParserError):
        command.parse_args(args)


def test_parse_arg_invalid_type() -> None:
    """Test that an error is raised if an argument is of the wrong type."""
    command = Command(
        name="hello",
        fn=hello,
        signature=inspect.signature(hello),
        doc="",
    )
    args = ["John", "invalid"]

    with pytest.raises(ArgumentParserError):
        command.parse_args(args)
