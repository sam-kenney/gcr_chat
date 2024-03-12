"""Example entry point."""

from __future__ import annotations

if __name__ == "__main__":
    import sys

    sys.exit("python -m uvicorn examples.server:app --reload --port 8080")

import os

import fastapi
import httpx

from gcr_chat import (
    Bot,
    BotError,
    PubSubChatRequest,
)

# Set if you want to send responses to a webhook channel.
webhook = os.getenv("WEBHOOK_URL")

app = fastapi.FastAPI()
bot = Bot("!", prefix_sep="")


@bot.command
def greet(name: str, count: int = 1) -> str:
    """Greet a user."""
    return f"Hello, {name}! " * count


@bot.command
def int_sum(a: int, b: int) -> str:
    """Add two numbers together."""
    return f"{a + b}"


@bot.command(name="float sum")
def add_floats(a: float, b: float) -> str:
    """Add two floating point numbers together."""
    return f"{a + b}"


def reply_to_message(url: str, message: str) -> httpx.Response:
    """Post a message to a webhook."""
    return httpx.post(
        url,
        headers={"Content-Type": "application/json"},
        json={"text": message},
    ).raise_for_status()


@app.post("/")
async def handle_request(message: PubSubChatRequest) -> fastapi.Response:
    """Handle a request."""
    headers = {"Content-Type": "text/plain"}
    try:
        content = await bot.run(str(message))

        if webhook:
            reply_to_message(
                url=webhook,
                message=content,
            )

        return fastapi.Response(
            content=content,
            status_code=httpx.codes.OK,
            headers=headers,
        )

    except BotError as e:
        return fastapi.Response(
            content=str(e),
            status_code=httpx.codes.BAD_REQUEST,
            headers=headers,
        )
