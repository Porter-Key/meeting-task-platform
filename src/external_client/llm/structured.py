from __future__ import annotations

from typing import Any


def with_structured_output(
    model: Any,
    schema: type[Any] | dict[str, Any],
    *,
    include_raw: bool = False,
    **kwargs: Any,
) -> Any:
    return model.with_structured_output(schema, include_raw=include_raw, **kwargs)
