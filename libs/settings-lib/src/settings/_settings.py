from settings.base import get_namespace

__all__ = [
    "APP_SETTINGS",
    "LOGGING_SETTINGS",
    "FASTAPI_SETTINGS",
    "UVICORN_SETTINGS",
    "DB_SETTINGS",
    "CELERY_SETTINGS",
    "GITHUB_SETTINGS",
]

APP_SETTINGS = get_namespace("app")
LOGGING_SETTINGS = get_namespace("logging")
FASTAPI_SETTINGS = get_namespace("fastapi")
UVICORN_SETTINGS = get_namespace("uvicorn")
DB_SETTINGS = get_namespace("database")
CELERY_SETTINGS = get_namespace("celery")
GITHUB_SETTINGS = get_namespace("github")
