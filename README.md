# GCR Chat

A simple chatbot framework for working with Google Cloud Run & PubSub messages.

## Exports

* `Bot` - The main bot class.
* `PubSubMessageRequest` - A wrapper around a PubSub message, decodes the message using `__str__`
* `BotException` - Base exception for the module, other exceptions inherit from this.
* `ArgumentParserError` - When the bot fails to parse provided arguments.
* `CommandNotFoundError` - When the bot cannot look up a function with the same name as the command provided.
* `InvalidArgumentsError` - When the provided arguments do not match the command function's expected arguments.

## Examples

See the [`examples`](/examples/) for a simple bot using [`fastapi`](https://fastapi.tiangolo.com/).
