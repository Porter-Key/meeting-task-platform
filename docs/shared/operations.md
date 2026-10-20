# Operations

## Runtime

Active runtime is Django + GraphQL + Celery.

Public domain: `https://taskmanage.example.com`

Backend listens locally only: `127.0.0.1:8765`

Frontend owns reverse proxy and HTTP->HTTPS behavior. Do not expose backend ports publicly.

## Local commands

HTTP app:

```bash
PYTHONPATH=src:. DJANGO_SETTINGS_MODULE=config.django.settings \
  uv run python -m django runserver 127.0.0.1:8765 --noreload
```

Celery worker:

```bash
PYTHONPATH=src:. DJANGO_SETTINGS_MODULE=config.django.settings \
  uv run celery -A celery_app:celery_app worker -Q taskmanagement \
  --loglevel=INFO --concurrency=2 --max-tasks-per-child=10 --prefetch-multiplier=1
```

Celery Beat:

```bash
PYTHONPATH=src:. DJANGO_SETTINGS_MODULE=config.django.settings \
  uv run celery -A celery_app:celery_app beat --loglevel=INFO \
  --scheduler django_celery_beat.schedulers:DatabaseScheduler \
  --schedule /var/lib/taskmanagement/django-celerybeat-schedule.db
```

## Systemd services

Registered units:

- `taskmanagement-http.service`
- `taskmanagement-celery.service`
- `taskmanagement-celery-beat.service`

Current service overrides switch the old FastAPI/orchestration runtime to Django:

- HTTP: `uv run python -m django runserver 127.0.0.1:8765 --noreload`
- Worker: `uv run celery -A celery_app:celery_app worker -Q taskmanagement ...`
- Beat: `uv run celery -A celery_app:celery_app beat --scheduler django_celery_beat.schedulers:DatabaseScheduler ...`

Common commands:

```bash
systemctl status taskmanagement-http.service
systemctl status taskmanagement-celery.service
systemctl status taskmanagement-celery-beat.service

systemctl restart taskmanagement-http.service
systemctl restart taskmanagement-celery.service
systemctl restart taskmanagement-celery-beat.service

journalctl -u taskmanagement-http.service -f
journalctl -u taskmanagement-celery.service -f
journalctl -u taskmanagement-celery-beat.service -f
```

## Validation

```bash
PYTHONPATH=src:. DJANGO_SETTINGS_MODULE=config.django.settings \
  uv run python -m compileall -q src/application src/django_client src/web/graphql

DJANGO_SETTINGS_MODULE=config.django.settings uv run python -m django check
DJANGO_SETTINGS_MODULE=config.django.settings uv run pytest
```

Health:

```bash
curl -fsS http://127.0.0.1:8765/health
```

GraphQL:

```bash
curl -fsS -X POST http://127.0.0.1:8765/graphql/ \
  -H 'Content-Type: application/json' \
  -H 'Host: taskmanage.example.com' \
  --data '{"query":"{ jobs(limit: 1) { id status } }"}'
```

GraphQL write smoke:

```bash
curl -fsS -X POST http://127.0.0.1:8765/graphql/ \
  -H 'Content-Type: application/json' \
  -H 'Host: taskmanage.example.com' \
  --data '{"query":"mutation($input: TaskCreateInput!){ createTaskMasterlistItem(input:$input){ id title status priority } }","variables":{"input":{"taskDate":"2026-05-24","title":"GraphQL smoke task","action":"Check mutation","context":"smoke","priority":"low","status":"draft","changedBy":"smoke"}}}'
```

Recent verified smoke covered:

- `createTaskMasterlistItem`
- `updateTaskMasterlistItem`
- `setTaskMondayFields`
- `archiveTaskMasterlistItems`
- `restoreTaskMasterlistItems`
- `submitTaskMasterlistItems`
- `upsertPerson`
- `upsertPersonAlias`

Celery worker:

```bash
PYTHONPATH=src:. DJANGO_SETTINGS_MODULE=config.django.settings \
  uv run celery -A celery_app:celery_app inspect ping --timeout=5
```

## Infra

Current production config uses existing localhost infra ports from `config/config.yaml`:

- PostgreSQL: `127.0.0.1:5433`
- Qdrant: `127.0.0.1:6333/6334`
- Redis/Celery broker: `127.0.0.1:6380`

The Django-local compose file still defines django-named containers/ports for isolated migration/testing. Production currently uses the existing server config values in `config/config.yaml`.

## Migrations applied

The runtime requires these Django package tables:

```bash
DJANGO_SETTINGS_MODULE=config.django.settings uv run python -m django migrate django_celery_results --noinput
DJANGO_SETTINGS_MODULE=config.django.settings uv run python -m django migrate django_celery_beat --noinput
```

## Notes for frontend

- Use `/graphql/` for all business reads/writes.
- `/health` is the only non-GraphQL public backend endpoint needed by frontend/proxy checks.
- Old `/queries/*` and `/commands/*` routes are gone.
- Keep proxying to backend on `127.0.0.1:8765`.
- Task/people GraphQL writes are synchronous Django ORM mutations; meeting pipeline mutations enqueue Celery jobs.
- Use camelCase in GraphQL requests, including inputs such as `taskDate`, `changedBy`, `mondayFieldValues`, `ownerEmail`.
