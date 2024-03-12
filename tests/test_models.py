"""Test the application models."""

from __future__ import annotations

from gcr_chat.models import PubSubChatRequest


def test_from_string() -> None:
    """Test the :meth:`from_string` classmethod."""
    content = "Hello, world!"
    model = PubSubChatRequest.from_string(content)

    assert str(model) == content
