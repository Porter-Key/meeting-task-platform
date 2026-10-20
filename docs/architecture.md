# 架构说明（Django 迁移后现状）

> 历史背景：本项目从自维护 PSQL + 独立编排层迁移到 Django 主运行时
> （见 `docs/architecture/django-target-architecture.md` 的迁移目标）。
> 迁移完成后，旧边界 `infra/psql`、`application/gate/*`、`orchestration/`、
> `interface/` 均已删除（顶层 `orchestration/` 死代码于公开快照前清理），
> Neo4j runtime 已下线。本文件描述当前实际结构。

## 目录结构

```text
src/
├── domain/              # 领域层：models（Django ORM）+ rules（纯规则）
├── application/
│   ├── use_case/        # 业务用例：meeting / monday / task_masterlist / beat
│   ├── tasks/           # Celery task 注册处（thin，直接调 use_case / workflow）
│   ├── event/           # LLM 事件流水线各阶段服务
│   ├── fireflies/       # Fireflies 拉取/入库服务
│   ├── meeting_wash/    # 转录清洗
│   ├── task_masterlist/ # 主清单同步/写服务
│   └── locks/           # 分布式锁
├── django_client/       # 基础设施①：Django 侧能力（ORM 查询写入、UoW 事务、
│                        # meeting/job/lifecycle/task_masterlist/monday/logs）
├── django_workflow/     # 多用例组装：meeting_pipeline / monday_sync /
│                        # task_masterlist_publish / beat_dispatch
├── external_client/     # 基础设施②：非 Django 外部服务
│                        # （fireflies / monday / llm / qdrant / cache / config）
├── web/                 # HTTP 层：GraphQL schema/queries/mutations、views
├── admin.py / apps.py / urls.py / celery_app.py
└── migrations/
```

## 核心结论：只剩两种基础设施

迁移后基础设施收敛为两类，再无其他 infra 抽象：

| # | 基础设施 | 位置 | 管什么 |
|---|---|---|---|
| ① | Django 侧 | `django_client/` | ORM 查询写入、事务边界（UoW）、本地状态 |
| ② | 外部服务 | `external_client/` | Fireflies、Monday、LLM/Embedding、Qdrant、缓存 |

- PSQL 已由 Django ORM 接管，不再手写 engine/session。
- `application/use_case` 只调这两类 infra + `domain/rules`，不关心依赖装配。
- `web/`（HTTP）与 `application/tasks/`（Celery）同属 Django 运行时，直接进
  `django_client`，不再经过编排/网关中间层。

## 调用关系

```text
HTTP          -> web/ -> django_client / application.tasks.delay()
Celery        -> application/tasks/*.py -> use_case/* 或 django_workflow/*
Use case      -> django_client + external_client + domain/rules
Django client -> domain/models + domain/rules
```

禁止方向：`domain -> application/web/Celery/external_client`，
`external_client -> django_client`。
