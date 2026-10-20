from __future__ import annotations

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.django.settings")

celery_app = Celery("taskmanagement")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks(["application"])
celery_app.conf.imports = (
    "application.tasks.beat",
    "application.tasks.meeting",
    "application.tasks.monday",
    "application.tasks.task_masterlist",
)
