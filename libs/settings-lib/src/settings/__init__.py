from __future__ import annotations

from ._settings import (
    FASTAPI_SETTINGS,
    UVICORN_SETTINGS,
    APP_SETTINGS,
    CELERY_SETTINGS,
    DB_SETTINGS,
    LOGGING_SETTINGS,
    GITHUB_SETTINGS,
)

from .base import SETTINGS, get_namespace
