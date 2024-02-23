"""Call the example `main.py` endpoint."""
import base64

import httpx

url = "http://localhost:8080/"


def encode(s: str) -> str:
    """Encode a message to send to the endpoint."""
    return base64.b64encode(s.encode("utf8")).decode("utf-8")


def call() -> None:
    """Call the endpoint."""
    resp = httpx.post(
        url,
        json={
            "message": {
                "data": encode("hello"),
            },
        },
    )

    print(resp.text)  # noqa: T201
    # "Hello, world!"

    resp = httpx.post(
        url,
        json={
            "message": {
                "data": encode("hello me 4"),
            },
        },
    )

    print(resp.text)  # noqa: T201
    # "Hello, me! Hello, me! Hello, me! Hello, me!"


if __name__ == "__main__":
    call()
