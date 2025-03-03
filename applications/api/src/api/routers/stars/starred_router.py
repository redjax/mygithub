from __future__ import annotations

import typing as t

from api import helpers as api_helpers
from api.responses import API_RESPONSE_DICT

from fastapi import APIRouter, Depends, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse, JSONResponse, Response, StreamingResponse
from loguru import logger as log

__all__ = ["router"]

prefix: str = "/stars"

tags: list[str] = ["stars"]

router: APIRouter = APIRouter(prefix=prefix, responses=API_RESPONSE_DICT, tags=tags)


@router.get("/")
def get_root():
    return {"msg": "hello, world"}
