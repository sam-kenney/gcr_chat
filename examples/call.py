"""Call the example `main.py` endpoint."""

from __future__ import annotations

import httpx

from gcr_chat import PubSubChatRequest

url = "http://localhost:8080/"


def call() -> None:
    """Call the endpoint."""
    resp = httpx.post(
        url,
        json=PubSubChatRequest.from_string("!greet me").model_dump(),
    )

    print(resp.text)  # noqa: T201
    # "Hello, me! "

    resp = httpx.post(
        url,
        json=PubSubChatRequest.from_string("!greet me 4").model_dump(),
    )

    print(resp.text)  # noqa: T201
    # "Hello, me! Hello, me! Hello, me! Hello, me! "

    resp = httpx.post(
        url,
        json=PubSubChatRequest.from_string("!int sum 2 4").model_dump(),
    )

    print(resp.text)  # noqa: T201
    # "6"

    resp = httpx.post(
        url,
        json=PubSubChatRequest.from_string("!float sum 6 2.2").model_dump(),
    )

    print(resp.text)  # noqa: T201
    # "8.2"


if __name__ == "__main__":
    call()
