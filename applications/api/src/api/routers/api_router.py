from __future__ import annotations

from api.responses import API_RESPONSE_DICT

from .healthcheck import router as healthcheck_router

# from .weather.weather_router import router as weather_router
from .stars.starred_router import router as stars_router
from .search.search_router import router as search_router

from fastapi import APIRouter
from loguru import logger as log
from settings.api_settings import FASTAPI_SETTINGS

__all__ = ["router"]

prefix: str = "/api/v1"

router: APIRouter = APIRouter(prefix=prefix, responses=API_RESPONSE_DICT)

INCLUDE_ROUTERS: list[APIRouter] = [
    healthcheck_router,
    stars_router,
    search_router
]

for _router in INCLUDE_ROUTERS:
    router.include_router(_router)
