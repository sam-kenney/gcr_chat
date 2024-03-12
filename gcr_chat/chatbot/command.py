"""Command model for the bot."""

from __future__ import annotations

import inspect
import logging
from collections.abc import Callable  # noqa: TCH003
from typing import (
    Any,
    get_type_hints,
)

import pydantic

from gcr_chat.chatbot.exceptions import ArgumentParserError

logger = logging.getLogger(__name__)


class Command(pydantic.BaseModel):
    """Command model for the bot."""

    name: str
    fn: Callable
    signature: inspect.Signature
    doc: str = ""
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)

    def parse_args(self, args: list[str]) -> list[Any]:
        """
        Parse arguments expected to be passed to a command.

        Converts each argument from a string to the type
        specified in the function signature.

        Params
        ------
        args: :class:`list[str]`
            The arguments to parse.

        Returns
        -------
        :class:`list[Any]`
            The parsed arguments

        Raises
        ------
        :class:`ArgumentParserError`
            If an argument could not be parsed.
        :class:`ArgumentParserError`
            If the number of arguments provided does not match
            the number of arguments expected.
        """
        parsed_args = []
        if len(args) != len(self.signature.parameters):
            for i, param in enumerate(self.signature.parameters.values()):
                param_has_default = param.default is not inspect.Parameter.empty
                param_provided = i < len(args)

                if not param_has_default and not param_provided:
                    error = (
                        f"Expected {len(self.signature.parameters)} arguments, "
                        f"but received {len(args)}."
                    )
                    logger.critical(error)
                    raise ArgumentParserError(error)

                if param_has_default and not param_provided:
                    args.append(param.default)

        for arg, dtype in zip(args, get_type_hints(self.fn).values(), strict=False):
            try:
                parsed_args.append(dtype(arg))
            except ValueError as e:  # noqa: PERF203
                logger.debug(e)
                error = f"Could not convert {arg} to {dtype.__name__}."
                logger.critical(error)
                raise ArgumentParserError(error) from e

        return parsed_args
