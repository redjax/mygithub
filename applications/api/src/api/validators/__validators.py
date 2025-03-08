from __future__ import annotations

from fastapi import APIRouter
from loguru import logger as log

__all__ = [
    "is_str",
    "is_list_str",
    "validate_root_path",
    "validate_router",
    "validate_openapi_tags",
]


def is_str(input: str) -> str | None:
    if not input:
        return None

    if not isinstance(input, str):
        try:
            eval_input: str = str(input)
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception convering input from type({type(input)}) to type(str). Details: {exc}"
            )
            log.error(msg)

            raise exc

    return eval_input


def is_list_str(_list: list[str]) -> list[str]:
    if not _list:
        raise ValueError("Missing input list to evaluate")

    if not isinstance(_list, list):
        raise ValueError("Input list must be of type list")

    for _i in _list:
        if not isinstance(_i, str):
            raise ValueError(
                f"Non-str list item ({type(_i)}): {_i}. List items must be of type str"
            )

    return _list


def validate_root_path(root_path: str) -> str:
    if not root_path:
        raise ValueError("Missing root_path value")
        
    evaluated_root_path: str | None = is_str(root_path)
    
    if not evaluated_root_path:
        raise ValueError(f"root_path validation returned None, indicating the input value could not be converted to a string. Input value ({type(root_path)}): {root_path}")

    return evaluated_root_path


def validate_openapi_tags(_tags: list[dict]) -> list[dict]:
    if not _tags:
        raise ValueError("Missing list of tag dicts to evaluate")

    if not isinstance(_tags, list):
        raise ValueError("Input object must be of type list")

    for _i in _tags:
        if not isinstance(_i, dict):
            raise ValueError(
                f"Non-dict list item ({type(_i)}): {_i}. List items must be of type dict"
            )

    return _tags


def validate_router(router: APIRouter, none_ok: bool = False) -> APIRouter:
    if not router:
        if not none_ok:
            raise ValueError("Missing APIRouter to evaluate")

    if not isinstance(router, APIRouter):
        raise TypeError(
            f"Invalid router type: {type(router)}. Must be of type(APIRouter)"
        )

    return router
