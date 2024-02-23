"""A simple chatbot framework."""
from __future__ import annotations

import functools
import inspect
import logging
from typing import TYPE_CHECKING, Any

from gcr_chat.chatbot.command import Command
from gcr_chat.chatbot.exceptions import (
    ArgumentParserError,
    CommandNotFoundError,
    InvalidArgumentsError,
)

if TYPE_CHECKING:
    from collections.abc import Callable

logger = logging.getLogger(__name__)


class Bot:
    """A simple chatbot framework."""

    def __init__(self, prefix: str = "!", prefix_sep: str = "") -> None:
        """
        # Chat bot.

        Params
        ------
        prefix: :class:`str`
            The command prefix.

        prefix_sep: :class:`str`
            The seperator between the prefix and the
            command name. E.G, `prefix_sep=''` would work
            with something like `!command`, `or prefix_sep=' '`
            would work with something like `@bot command`
        """
        self.prefix = f"{prefix}{prefix_sep}"
        self.commands: list[Command] = [
            Command(
                name="help",
                fn=self.help_,
                signature=inspect.signature(self.help_),
                doc=self.help_.__doc__ or "",
            ),
        ]

    def help_(self) -> str:
        """Display the help message."""
        return "\n".join([self.usage(c) for c in self.commands])

    def usage(self, command: Command) -> str:
        """Get the usage string for a command."""
        args = []

        for arg in command.signature.parameters.values():
            if arg.default is inspect.Parameter.empty:
                args.append(f"<{arg.name}: {arg.annotation}>")
            else:
                args.append(f"optional(<{arg.name}: {arg.annotation} = {arg.default}>)")

        msg = "\n    " + "\n    ".join(args) + "\n" if args else "\n"

        return f"{self.prefix}{command.name}: {command.doc}{msg}"

    def command(self, fn: Callable | None = None, name: str | None = None) -> Callable:
        """
        Register a function as a command.

        Params
        ------
        fn: :class:`Callable`
            The function to register as a command.

        name: :class:`str | None`
            An optional override for the command name.
            If not specified, the command name will be
            the funciton name with underscores replaced
            with spaces.
        """

        def wrap_command(f: Callable) -> Callable:
            # Allows for calling decorator with or without parens
            @functools.wraps(f)
            def register(*_args: Any, **_kwargs: Any) -> Callable:
                """Register the function as a command."""
                command = Command(
                    name=name or fn.__name__.replace("_", " "),
                    fn=f,
                    signature=inspect.signature(f),
                    doc=fn.__doc__ or "",
                )

                self.commands.append(command)

                msg = (
                    f"Registered function {command.name} with "
                    f"signature {command.signature}"
                )
                logger.debug(msg)
                return f

            return register(f)

        if fn:
            return wrap_command(fn)

        return wrap_command

    def _lookup_command(self, raw: list[str]) -> tuple[Command, list[str]]:
        """
        Lookup a command from a list of strings.

        Params
        ------
        raw: :class:`list[str]`
            The list of strings to lookup.

        Returns
        -------
        :class:`tuple[Command, list[str]]`
            The command and the remaining arguments.

        Raises
        ------
        :class:`CommandNotFoundError`
            If the command could not be found.
        """
        cmd_name = []

        for i, s in enumerate(raw):
            cmd_name.append(s)
            cmd = next(
                filter(lambda x: x.name == " ".join(cmd_name), self.commands),
                None,
            )

            if cmd is not None:
                return cmd, raw[i + 1 :]

        error = (
            f"Command {' '.join(cmd_name)} could not be parsed "
            "or is not registered in app"
        )

        logger.critical(error)
        raise CommandNotFoundError(
            f"Command {' '.join(raw)} is not valid or does not exist.\n"
            "Valid commands are:\n" + "\n".join([self.usage(c) for c in self.commands]),
        )

    def _clean_command(self, command_string: str) -> str:
        """
        Clean a command.

        Params
        ------
        command_string: :class:`str`
            The command to clean.

        Returns
        -------
        :class:`str`
            The cleaned command.
        """
        return " ".join(
            command_string.strip().replace(f"{self.prefix}", "").split(),
        )

    async def run(self, command_string: str) -> str:
        """
        Run a command.

        Params
        ------
        command_string: :class:`str`
            The command to run with its arguments.

        Returns
        -------
        :class:`str`
            The result of the command.

        Raises
        ------
        :class:`CommandNotFoundError`
            If the command could not be found.
        :class:`InvalidArgumentsError`
            If the command was called with invalid arguments.
        :class:`ArgumentParserError`
            If the command arguments could not be parsed.
        """
        command, args = self._lookup_command(
            self._clean_command(command_string).split(" "),
        )

        parsed_args = command.parse_args(args)

        try:
            if inspect.iscoroutinefunction(command.fn):
                return await command.fn(*parsed_args)

            return command.fn(*parsed_args)

        except TypeError as e:
            error = (
                f"Command {command.name} called with invalid arguments {args}. "
                f"Expected {command.signature}"
            )
            logger.critical(error)
            raise InvalidArgumentsError(
                "The provided arguments do not match the command signature.\n"
                + self.usage(command),
            ) from e
        except ArgumentParserError as e:
            raise ArgumentParserError(f"{e}\n{self.usage(command)}") from e
