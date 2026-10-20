# `src/` — Django runtime

This package is the runnable application: meeting ingestion → cleanup (“wash”) →
LLM event extraction → task masterlist → Monday sync, exposed over GraphQL
(Strawberry), a few REST views, and the Django admin.

Entry points: `urls.py` → `web/urls.py` (GraphQL schema, views, admin),
`celery_app.py` + `application/tasks/` (Celery workers / beat),
`apps.py` (`TaskManagementConfig`).

## Layout

```text
src/
├── domain/                  # Domain layer: models + rules, no framework imports
│   ├── models/              # meeting, event, people, monday, task_masterlist, job, lifecycle, logs
│   └── rules/               # lifecycle state machine (allowed transitions, canonical
│                            # statuses), meeting lifecycle, retry policy
├── application/             # Business logic
│   ├── event/               # LLM event pipeline: topic_extract → event_draft →
│   │                        #   event_refine → people_tasks → tl_dr (+ prompts, schemas,
│   │                        #   fact_layer, vector, people_normalization)
│   ├── fireflies/           # Fireflies ingest/pull services + schemas
│   ├── meeting_wash/        # Transcript cleanup: chunking, normalize, cleanup, ai_cleanup
│   ├── task_masterlist/     # Masterlist sync/write services
│   ├── tasks/               # Celery tasks: meeting, monday, task_masterlist, beat
│   ├── use_case/            # Callable use-case entry points (pure functions of payload dicts):
│   │                        #   meeting/{ingest,wash,generate_events,regenerate,manage,delete,
│   │                        #   upsert_person}, monday/{sync_users,sync_structure,associate_identity},
│   │                        #   task_masterlist/{submit,publish,rebuild}, beat/dispatch
│   ├── people_extraction.py # People extraction from meetings
│   └── locks/               # Distributed locking
├── django_client/           # Django-bound adapters: repositories, UnitOfWork, per-domain
│                            # clients (meeting, monday, people, task_masterlist, job, logs…)
├── django_workflow/         # Thin runners wiring use cases into Django/Celery, e.g.
│                            # run_meeting_pipeline: ingest → wash → generate_events
├── external_client/         # Third-party clients + config loader:
│                            #   fireflies / monday / llm (chat, embeddings, structured,
│                            #   streaming, vectorstores, cache) / qdrant / cache / config
├── web/                     # Interface: GraphQL schema/queries/mutations/DTOs (incl.
│                            #   TodayApi), serializers, views, urls
├── interface/               # Reserved for future interface adapters (empty)
├── migrations/              # Django migrations
├── admin.py / apps.py / urls.py / celery_app.py
```

## Core flows

1. **Meeting pipeline** (`django_workflow/meeting_pipeline.py`):
   `ingest_meeting` (Fireflies pull → transcripts → people upsert → lifecycle `ingested`)
   → `wash_meeting` (chunk → normalize → cleanup)
   → `generate_events` (`EventGenerationPipeline`: topics → draft → refine →
   people tasks → TL;DR → conclusion saved, lifecycle `conclusion_generated` /
   `task_extracted`).
2. **Masterlist → Monday** (`use_case/task_masterlist/{submit,publish,rebuild}` +
   `use_case/monday/sync_*`): review working list, publish, sync users/structure/identity.
3. **Beat dispatch** (`application/tasks/beat.py` → `django_workflow/beat_dispatch.py`):
   scheduled sweep with autoretry + backoff.

## Cross-cutting conventions

- **Lifecycle marks**: every stage transition goes through
  `domain/rules/lifecycle.can_change_state(...)` and is recorded with a decision +
  reason — the audit trail for “why is this meeting in this state”.
- **Correlation IDs**: pipeline stages log `event_pipeline_started/completed`-style
  structured events with `correlation_id` + `meeting_id`.
- **Use cases are plain functions** taking/returning `payload: dict`; Django/ORM
  access lives in `django_client/`, third-party access in `external_client/`.
- **Config**: copy `config/config.example.yaml` → `config/config.yaml`
  (gitignored, never commit real keys). Infra examples: `dockers/`.
