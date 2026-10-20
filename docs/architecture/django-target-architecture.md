# Django 目标架构

本文描述本 worktree 的一次性 Django 化重构目标。

## 结论

Django 是主运行时，负责 ORM、事务、HTTP、Celery 集成、Admin、日志查询和任务创建。

旧结构中的 `infra/psql`、`application/gate/dependency`、`orchestration`、`interface` 不再作为长期边界保留。

## 目标目录

```text
src/
  apps.py
  admin.py
  urls.py
  celery_app.py
  migrations/

  domain/
    models/
      base.py
      meeting.py
      job.py
      lifecycle.py
      event.py
      task_masterlist.py
      logs.py
      monday.py
    rules/
      lifecycle.py
      meeting_lifecycle.py
      retry.py

  django_client/
    __init__.py
    uow.py
    meeting.py
    job.py
    lifecycle.py
    task_masterlist.py
    monday.py
    logs.py

  application/
    use_case/
      meeting/
      task_masterlist/
      monday/
      beat/
    tasks/
      meeting.py
      task_masterlist.py
      monday.py
      beat.py

  django_workflow/
    meeting_pipeline.py
    monday_sync.py
    task_masterlist_publish.py
    beat_dispatch.py

  external_client/
    qdrant/
    monday/
    fireflies/
    llm/

  web/
    urls.py
    views.py
    serializers.py

config/
  django/
    settings.py
    asgi.py
    wsgi.py
```

## 模块职责

### `src/apps.py`

Django app 注册入口。

负责：

- 定义 `AppConfig`。
- 设置 app label，例如 `taskmanagement`。
- 挂载 signals 或启动检查。

### `src/admin.py`

Django Admin 注册入口。

用于本地调试和运营检查：

- Job
- Lifecycle / PipelineRun
- ApplicationLog
- Meeting
- TaskMasterlist
- Monday mapping

### `src/urls.py`

项目内根路由。

一般只 include：

- `web.urls`
- Django admin
- 健康检查路由

### `src/celery_app.py`

Django Celery app 入口。

负责：

- 从 `config.django.settings` 读取 Celery 配置。
- autodiscover `application.tasks`。
- 配置 result backend、broker、retry 默认值。

### `src/migrations/`

Django schema migration 文件。

重构初期可以先映射现有表，跑通后再清理字段和 migration 历史。

---

## `domain/`

`domain` 是 Django 化后的业务数据和规则核心。

### `domain/models/`

Django ORM models，替换旧：

- `infra/psql/models/*`
- `domain/models/logs.py`
- 与 PSQL 相关的 SQLAlchemy ORM

职责：

- 表结构。
- model method。
- manager/queryset。
- 轻量状态字段定义。

不放：

- 外部 API 调用。
- Celery task。
- 大型流程编排。

建议文件：

| 文件 | 职责 |
|---|---|
| `base.py` | 通用时间戳、软删除、公共 manager |
| `meeting.py` | Meeting、Transcript、Chunk、Topic、Conclusion、People candidate/link |
| `job.py` | ApplicationJob、异步任务状态、payload/result/error |
| `lifecycle.py` | PipelineRun、LifecycleEvent、Beat/Schedule 状态 |
| `event.py` | Event、MeetingEvent、事件关系、owner、qdrant point id |
| `task_masterlist.py` | 任务主清单、归档、发布状态、Monday target |
| `logs.py` | ApplicationLog、结构化日志 |
| `monday.py` | Monday board/group/column/user/item mapping |

### `domain/rules/`

纯规则层，不直接写数据库。

职责：

- 生命周期状态转换。
- 会议是否需要处理。
- 重试判断。
- 终态/运行态/可重试态判断。

建议文件：

| 文件 | 职责 |
|---|---|
| `lifecycle.py` | allowed transitions、canonical status、terminal/running 判断 |
| `meeting_lifecycle.py` | meeting 是否可处理、是否可重跑、stale running 判断 |
| `retry.py` | max attempts、retryable exception、backoff decision |

---

## `django_client/`

`django_client` 是 Django 暴露给 application 的高内聚业务入口。

它替代旧 repo 层和一部分 service 层。

职责：

- 封装 Django ORM 查询和写入。
- 注册 UoW / transaction 能力。
- 对 use case 暴露稳定 API。
- 聚合 model + rules。

不做：

- HTTP request/response 处理。
- Celery task 注册。
- 外部 API 细节。

建议文件：

| 文件 | 职责 |
|---|---|
| `uow.py` | `transaction.atomic()`、UoW registry、跨 client 的事务边界 |
| `meeting.py` | 会议保存、查询、删除、重跑准备 |
| `job.py` | create job、attach celery task id、mark running/completed/failed、progress |
| `lifecycle.py` | mark lifecycle、record pipeline run、query latest lifecycle、cleanup stale |
| `task_masterlist.py` | task masterlist CRUD、archive/restore、publish state |
| `monday.py` | Monday 本地映射缓存读写 |
| `logs.py` | ApplicationLog 写入和查询 |

示意：

```python
from django.db import transaction

class UoW:
    def atomic(self):
        return transaction.atomic()

uow = UoW()
```

---

## `application/`

`application` 只保留用例和 Celery task。

不再有：

- `gate/dependency`
- `gate/function`
- dependency container

### `application/use_case/`

业务用例编排。

职责：

- 表达一个业务动作。
- 调用 `django_client`。
- 调用 `external_client`。
- 使用 `domain/rules` 的结果。

示例：

```text
application/use_case/meeting/ingest.py
application/use_case/meeting/wash.py
application/use_case/meeting/generate_events.py
application/use_case/task_masterlist/publish.py
application/use_case/monday/sync_users.py
```

### `application/tasks/`

Celery tasks 直接定义处。

这里的 `tasks` 就是 Celery task，不再另设 `django_tasks`。

职责：

- `@shared_task` 注册。
- 配置 retry/backoff。
- 调用 `application/use_case` 或 `django_workflow`。
- 写 job/lifecycle/log 状态。

示意：

```python
from celery import shared_task
from application.use_case.meeting.ingest import ingest_meeting

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True)
def ingest_meeting_task(self, payload: dict):
    return ingest_meeting(payload)
```

调试方式：启动 Celery worker。

---

## `django_workflow/`

多步骤 workflow 组装层。

职责：

- 串联多个 use case。
- 表达端到端流程。
- 不直接写复杂 ORM。

示例：

```text
django_workflow/meeting_pipeline.py
  ingest -> wash -> generate_events -> lifecycle completed

django_workflow/monday_sync.py
  sync users -> sync structure -> associate identity

django_workflow/task_masterlist_publish.py
  validate -> build payload -> publish -> mark result

django_workflow/beat_dispatch.py
  find due schedules -> create jobs -> enqueue celery tasks
```

---

## `external_client/`

所有非 Django 数据库的外部服务客户端。

职责：

- Qdrant
- Monday API
- Fireflies API
- LLM / Embedding

不放：

- PSQL client。
- Django ORM。
- Celery task。

PSQL 已经由 Django ORM 接管。

---

## `web/`

Django HTTP 层。

职责：

- 查询。
- 创建任务。
- 看日志。
- 看进度。

典型接口：

```text
GET  /jobs/
GET  /jobs/<id>/
GET  /jobs/<id>/logs/
POST /jobs/meeting-pipeline/
POST /jobs/monday-sync/
GET  /meetings/
GET  /meetings/<id>/
GET  /logs/
```

调用关系：

```text
web/views.py
  -> django_client.job.create(...)
  -> application.tasks.meeting.run_pipeline.delay(job_id, payload)
  -> django_client.logs.list(...)
  -> django_client.lifecycle.progress(...)
```

Web 不需要绕过 Django；查询、创建任务、看日志都由 Django 原生负责。

---

## `config/django/`

Django 项目配置。

职责：

- DB settings。
- Celery settings。
- installed apps。
- logging。
- middleware。
- external config bridge。

建议保留现有 `config/config.yaml` 作为本地业务配置来源；Django settings 读取其中外部 API、Qdrant、LLM 等配置。

---

## 调用方向

```text
HTTP
  -> web/views.py
  -> django_client / application.tasks.delay()

Celery
  -> application/tasks/*.py
  -> application/use_case/* 或 django_workflow/*
  -> django_client
  -> domain/models + domain/rules

Use case
  -> django_client
  -> external_client
  -> domain/rules

Django client
  -> domain/models
  -> domain/rules
```

禁止方向：

```text
domain -> application
domain -> web
domain -> Celery
domain -> external_client
external_client -> django_client
```

---

## 相比旧架构的变化

删除长期边界：

- `infra/psql`
- `application/gate/dependency`
- `application/gate/function`
- `orchestration`
- `interface`
- Neo4j 相关 runtime

收敛为：

- Django ORM + transaction。
- `django_client` 高内聚业务入口。
- `application/use_case` 用例。
- `application/tasks` Celery task。
- `web` Django HTTP。
- `external_client` 外部服务。

主要收益：

- 不再手写 PSQL engine/session/session_scope。
- Celery、HTTP、Admin、日志、ORM 同运行时。
- Job/Lifecycle/Logs 成为 Django model，一处查询和管理。
- use case 不再关心依赖装配。
- 调试路径缩短：Django shell/admin + Celery worker。
