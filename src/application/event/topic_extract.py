from __future__ import annotations

from typing import Any
from concurrent.futures import ThreadPoolExecutor, as_completed

from external_client.llm.structured import with_structured_output

from .fact_layer import build_fact_layer
from .topic_prompts import topic_prompt
from .schemas import TopicExtractionSchema
from .topic_cluster import filter_event_worthy_topics, semantic_chunk_clusters, topic_text


DEFAULT_EVENT_WORKERS = 64


class TopicExtractionService:
    def __init__(self, chat_model: Any, embeddings: Any, logger: Any | None = None) -> None:
        self.topic_extractor = with_structured_output(chat_model, TopicExtractionSchema)
        self.embeddings = embeddings
        self.max_workers = DEFAULT_EVENT_WORKERS
        self.logger = logger

    def extract_topics(self, meeting: dict[str, Any], chunks: list[dict[str, Any]], *, debug: bool = False, correlation_id: str | None = None) -> list[dict[str, Any]]:
        if debug and self.logger:
            self.logger.trace_call("TopicExtractionService.extract_topics.input", input={"meeting": meeting, "chunks": chunks}, stage="event_debug", correlation_id=correlation_id, meeting_id=meeting.get("id"))
        topics: list[dict[str, Any]] = []
        clusters = semantic_chunk_clusters(self.embeddings, chunks)
        if debug and self.logger:
            self.logger.trace_call("TopicExtractionService.semantic_chunk_clusters.output", output=clusters, stage="event_debug", correlation_id=correlation_id, meeting_id=meeting.get("id"))
        def extract_cluster(cluster: dict[str, Any]) -> list[dict[str, Any]]:
            cluster_chunks = [chunks[idx] for idx in cluster["chunk_indexes"]]
            if debug and self.logger:
                self.logger.trace_call("TopicExtractionService.extract_cluster.input", input={"cluster": cluster, "cluster_chunks": cluster_chunks}, stage="event_debug", correlation_id=correlation_id, meeting_id=meeting.get("id"))
            fact_layer = build_fact_layer(meeting, cluster_chunks, max_facts=24)
            parsed = self.topic_extractor.invoke([("system", "You generate exactly one Topic for each HDBSCAN batch. Use the fact layer to avoid factual errors."), ("human", topic_prompt(meeting, cluster_chunks, fact_layer))])
            payload = TopicExtractionSchema.model_validate(parsed.model_dump() if hasattr(parsed, "model_dump") else parsed).model_dump()
            topic = payload.get("topic") or {}
            topic["semantic_cluster_id"] = cluster["cluster_id"]
            topic["representative_chunk_indexes"] = cluster["representative_indexes"]
            topic["source_chunk_indexes"] = cluster["chunk_indexes"]
            topic["chunk_indexes"] = cluster["chunk_indexes"]
            topic["vector_text"] = topic_text(topic)
            cluster_topics = [topic]
            if debug and self.logger:
                self.logger.trace_call("TopicExtractionService.extract_cluster.output", output=cluster_topics, stage="event_debug", correlation_id=correlation_id, meeting_id=meeting.get("id"))
            return cluster_topics

        ordered: list[list[dict[str, Any]] | None] = [None] * len(clusters)
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(extract_cluster, cluster): idx for idx, cluster in enumerate(clusters)}
            for future in as_completed(futures):
                ordered[futures[future]] = future.result()
        for group in ordered:
            topics.extend(group or [])
        filtered = filter_event_worthy_topics(topics)
        if debug and self.logger:
            self.logger.trace_call("TopicExtractionService.extract_topics.output", output=filtered, stage="event_debug", correlation_id=correlation_id, meeting_id=meeting.get("id"))
        return filtered
