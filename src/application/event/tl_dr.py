from __future__ import annotations

from typing import Any

from external_client.llm.structured import with_structured_output

from .conclusion_normalizer import selected_option_indexes
from .schemas import TlDrSchema
from .tl_dr_prompts import tl_dr_prompt


class TlDrService:
    def __init__(self, chat_model: Any, logger: Any | None = None) -> None:
        self.extractor = with_structured_output(chat_model, TlDrSchema)
        self.logger = logger

    def generate(self, meeting: dict[str, Any], topics: list[dict[str, Any]], conclusion: dict[str, Any], *, fact_layer: dict[str, Any] | None = None, debug: bool = False, correlation_id: str | None = None) -> dict[str, Any]:
        if debug and self.logger:
            self.logger.trace_call("TlDrService.generate.input", input={"meeting": meeting, "conclusion": conclusion}, stage="event_debug", correlation_id=correlation_id, meeting_id=meeting.get("id"))
        parsed = self.extractor.invoke([
            ("system", "You generate only tl_dr from refined events and people tasks."),
            ("human", tl_dr_prompt(meeting, conclusion, fact_layer)),
        ])
        payload = TlDrSchema.model_validate(parsed.model_dump() if hasattr(parsed, "model_dump") else parsed).model_dump()
        payload["tl_dr"] = [str(item).strip() for item in (payload.get("tl_dr") or []) if str(item).strip()][:5]
        payload["one_sentence_summary"] = str(payload.get("one_sentence_summary") or "").strip()
        payload["summary"] = str(payload.get("summary") or payload["one_sentence_summary"]).strip()
        if debug and self.logger:
            self.logger.trace_call("TlDrService.generate.output", output=payload, stage="event_debug", correlation_id=correlation_id, meeting_id=meeting.get("id"))
        return payload
