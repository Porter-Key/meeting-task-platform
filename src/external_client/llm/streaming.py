from __future__ import annotations

from collections.abc import AsyncIterator, Iterator, Sequence
from typing import Any

from langchain_core.messages import BaseMessage


def _chunk_to_text(chunk: Any) -> str:
    content = getattr(chunk, "content", chunk)
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    return str(content)


def stream_text(model: Any, messages: str | Sequence[BaseMessage] | Sequence[tuple[str, str]], **kwargs: Any) -> Iterator[str]:
    for chunk in model.stream(messages, **kwargs):
        text = _chunk_to_text(chunk)
        if text:
            yield text


async def astream_text(model: Any, messages: str | Sequence[BaseMessage] | Sequence[tuple[str, str]], **kwargs: Any) -> AsyncIterator[str]:
    async for chunk in model.astream(messages, **kwargs):
        text = _chunk_to_text(chunk)
        if text:
            yield text
