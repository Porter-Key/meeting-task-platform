# meeting-task-platform

Meeting intelligence → task pipeline. Pulls meeting transcripts (Fireflies),
cleans them up, extracts topics / events / people tasks with LLMs, keeps a
reviewable task masterlist, and syncs it to Monday. Every stage transition is
lifecycle-guarded and audit-logged, so you can always answer “why is this
meeting in this state”.

> Sanitized public snapshot: real credentials, deployment domains and client
> PII were removed; only `*.example.*` configs ship. See
> `config/config.example.yaml`, `dockers/docker-compose.example.yaml`.

## Stack

Python ≥ 3.11 · Django 5 + Django REST · Strawberry GraphQL · Celery + Beat ·
PostgreSQL (psycopg) · Redis · Qdrant · LangChain / OpenAI-compatible LLMs ·
pytest.

## Layout

```text
src/                    # Django runtime (see src/README.md for details)
├── domain/             # models + rules (lifecycle state machine, retry policy)
├── application/        # event pipeline, fireflies ingest, meeting wash,
│                       # task masterlist, celery tasks, use-case entry points
├── django_client/      # infra ①：Django 侧（ORM、事务、本地状态）
├── django_workflow/    # 多用例组装：ingest → wash → generate、beat dispatch…
├── external_client/    # infra ②：外部服务（fireflies/monday/llm/qdrant/cache）
└── web/                # GraphQL schema/queries/mutations, serializers, views
scripts/                # ops helpers (e.g. qdrant copy)
dockers/                # local infra (postgres / qdrant / redis)
config/                 # runtime config (example only — real config is gitignored)
docs/                   # architecture notes, vendor API references, plans
tests/                  # pytest suite (replay fixtures for lifecycle boundaries)
```

## Configure

```bash
cp config/config.example.yaml config/config.yaml        # fill in your keys
# local infra:
docker compose -f dockers/docker-compose.example.yaml up -d
```

`config.yaml` and `dockers/docker-compose.yaml` are gitignored — never commit
real secrets (that mistake was made once, hence this snapshot).

## Test

```bash
pytest   # pythonpath=src is set in pyproject.toml
```
