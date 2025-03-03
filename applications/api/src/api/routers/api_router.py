from __future__ import annotations

from api.responses import API_RESPONSE_DICT

from .healthcheck import router as healthcheck_router

# from .weather.weather_router import router as weather_router
from .stars.starred_router import router as stars_router

from fastapi import APIRouter
from loguru import logger as log
from settings.api_settings import FASTAPI_SETTINGS

__all__ = ["router"]

prefix: str = "/api/v1"

router: APIRouter = APIRouter(prefix=prefix, responses=API_RESPONSE_DICT)

router.include_router(healthcheck_router)
router.include_router(stars_router)
