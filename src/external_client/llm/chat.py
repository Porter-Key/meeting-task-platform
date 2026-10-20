from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI

from external_client.config import LLMProviderConfig


def create_chat_model(
    config: LLMProviderConfig,
    *,
    model: str | None = None,
    streaming: bool = True,
    temperature: float | None = None,
    **overrides: Any,
) -> ChatOpenAI:
    model_overrides = {"use_responses_api": False, **overrides}
    provider_extra = {key: value for key, value in config.extra.items() if key != "use_responses_api"}
    return ChatOpenAI(
        model=config.model_name(model),
        api_key=config.api_key,
        base_url=config.base_url,
        temperature=config.temperature if temperature is None else temperature,
        timeout=config.timeout_seconds,
        max_retries=config.max_retries,
        streaming=streaming,
        **provider_extra,
        **model_overrides,
    )


def invoke_text(model: Any, messages: str | Sequence[BaseMessage] | Sequence[tuple[str, str]], **kwargs: Any) -> str:
    result = model.invoke(messages, **kwargs)
    content = getattr(result, "content", result)
    return content if isinstance(content, str) else str(content)
