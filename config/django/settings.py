from __future__ import annotations

import os
from pathlib import Path
import sys
from urllib.parse import urlparse

import yaml

BASE_DIR = Path(__file__).resolve().parents[2]
PROJECT_ROOT = BASE_DIR
CONFIG_PATH = PROJECT_ROOT / "config" / "config.yaml"
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))


def _load_yaml() -> dict:
    if not CONFIG_PATH.exists():
        return {}
    with CONFIG_PATH.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


RAW_CONFIG = _load_yaml()


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _csv(value: str | None) -> list[str]:
    return [item.strip() for item in (value or "").split(",") if item.strip()]


_django_config = RAW_CONFIG.get("django", {})
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY") or _django_config.get("secret_key") or "dev-only-insecure-fallback-CHANGE-ME"
DEBUG = _env_bool("DJANGO_DEBUG", bool(_django_config.get("debug", False)))
ALLOWED_HOSTS = _csv(os.getenv("DJANGO_ALLOWED_HOSTS")) or list(_django_config.get("allowed_hosts") or ["taskmanage.example.com", "127.0.0.1", "localhost"])
CSRF_TRUSTED_ORIGINS = _csv(os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS")) or list(_django_config.get("csrf_trusted_origins") or ["https://taskmanage.example.com"])
ROOT_URLCONF = "urls"
WSGI_APPLICATION = "config.django.wsgi.application"
ASGI_APPLICATION = "config.django.asgi.application"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
USE_TZ = True
TIME_ZONE = "UTC"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_celery_results",
    "django_celery_beat",
    "apps.TaskManagementConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "DIRS": [],
        "OPTIONS": {"context_processors": [
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
        ]},
    }
]

_database = RAW_CONFIG.get("database") or RAW_CONFIG.get("infra", {}).get("psql", {})
_url = _database.get("connection_string")
if _url:
    parsed = urlparse(_url.replace("postgresql+psycopg://", "postgresql://"))
    DATABASES = {"default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": parsed.hostname or "127.0.0.1",
        "PORT": str(parsed.port or 5432),
        "USER": parsed.username or "thomas",
        "PASSWORD": parsed.password or "",
        "NAME": (parsed.path or "/taskmanagement").lstrip("/"),
    }}
else:
    DATABASES = {"default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": _database.get("host", "127.0.0.1"),
        "PORT": str(_database.get("port", 15433)),
        "USER": _database.get("username", "thomas"),
        "PASSWORD": _database.get("password", ""),
        "NAME": _database.get("database", "taskmanagement"),
    }}

_celery = RAW_CONFIG.get("infra", {}).get("celery", {})
broker_url = _celery.get("broker_url", "redis://127.0.0.1:16380/0")
CELERY_BROKER_URL = broker_url
broker_url = CELERY_BROKER_URL
CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "django-cache"
CELERY_TASK_DEFAULT_QUEUE = _celery.get("task_default_queue", "taskmanagement-django")
CELERY_TASK_ACKS_LATE = bool(_celery.get("task_acks_late", True))
CELERY_TASK_REJECT_ON_WORKER_LOST = bool(_celery.get("task_reject_on_worker_lost", True))
CELERY_WORKER_PREFETCH_MULTIPLIER = int(_celery.get("worker_prefetch_multiplier", 1))
CELERY_WORKER_MAX_TASKS_PER_CHILD = int(_celery.get("worker_max_tasks_per_child", 10))
broker_url = CELERY_BROKER_URL

STATIC_URL = "static/"
STATIC_ROOT = str(PROJECT_ROOT / "staticfiles")
SESSION_COOKIE_SECURE = _env_bool("DJANGO_SESSION_COOKIE_SECURE", bool(_django_config.get("session_cookie_secure", not DEBUG)))
CSRF_COOKIE_SECURE = _env_bool("DJANGO_CSRF_COOKIE_SECURE", bool(_django_config.get("csrf_cookie_secure", not DEBUG)))
SECURE_SSL_REDIRECT = _env_bool("DJANGO_SECURE_SSL_REDIRECT", bool(_django_config.get("secure_ssl_redirect", False)))
SECURE_HSTS_SECONDS = int(os.getenv("DJANGO_SECURE_HSTS_SECONDS") or _django_config.get("secure_hsts_seconds", 31536000 if not DEBUG else 0))
SECURE_HSTS_INCLUDE_SUBDOMAINS = _env_bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", bool(_django_config.get("secure_hsts_include_subdomains", not DEBUG)))
SECURE_HSTS_PRELOAD = _env_bool("DJANGO_SECURE_HSTS_PRELOAD", bool(_django_config.get("secure_hsts_preload", not DEBUG)))
SECURE_PROXY_SSL_HEADER = tuple(_django_config.get("secure_proxy_ssl_header") or ("HTTP_X_FORWARDED_PROTO", "https"))
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
LOGGING = {"version": 1, "disable_existing_loggers": False, "handlers": {"console": {"class": "logging.StreamHandler"}}, "root": {"handlers": ["console"], "level": "INFO"}}
