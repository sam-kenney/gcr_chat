"""Example entry point."""
from __future__ import annotations

import logging
import os

import fastapi
import httpx

from gcr_chat import (
    Bot,
    BotError,
    PubSubChatRequest,
)

logging.basicConfig(level=logging.CRITICAL)
logger = logging.getLogger(__name__)

# Set if you want to send responses to a webhook channel.
webhook = os.getenv("WEBHOOK_URL")

app = fastapi.FastAPI()
bot = Bot("!", prefix_sep="")


@bot.command
def hello(name: str = "world", count: int = 1) -> str:
    """Greet a user."""
    return f"Hello, {name}! " * count


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
        logger.critical(e)
        return fastapi.Response(
            content=str(e),
            status_code=httpx.codes.BAD_REQUEST,
            headers=headers,
        )


if __name__ == "__main__":
    import sys

    sys.exit("python -m uvicorn examples.main:app --reload --port 8080")
