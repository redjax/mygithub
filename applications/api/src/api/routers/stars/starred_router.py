from __future__ import annotations

import json
import math
import typing as t

from api import helpers as api_helpers
from api.pagination import PagedResponseSchema, PageParams
from api.responses import API_RESPONSE_DICT

import db_lib
from depends import db_depends
from domain.github import stars as stars_domain
from fastapi import APIRouter, Depends, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse, JSONResponse, Response, StreamingResponse
from loguru import logger as log
import sqlalchemy as sa
import sqlalchemy.exc as sa_exc
import sqlalchemy.orm as so

__all__ = ["router"]

prefix: str = "/stars"

tags: list[str] = ["stars"]

router: APIRouter = APIRouter(prefix=prefix, responses=API_RESPONSE_DICT, tags=tags)


@router.get("/all", response_model=None)
def return_all_stars(
    request: Request, page_params: PageParams = Depends()
) -> JSONResponse | PagedResponseSchema:
    session_pool = db_depends.get_session_pool()

    starred_repo_out_schemas: list[stars_domain.GithubStarredRepoOut] = []

    log.info("Retrieving all Github starred repositories")
    try:
        with session_pool() as session:
            repo = stars_domain.GithubStarredRepositoryDBRepository(session)

            total_count = repo.count()

            # Calculate offset and limit for pagination
            offset = (page_params.page - 1) * page_params.size
            limit = page_params.size

            # Fetch paginated results from the database
            all_starredrepo_models: list[stars_domain.GithubStarredRepositoryModel] = (
                repo.get_all_paginated(offset=offset, limit=limit)
            )

            if len(all_starredrepo_models) == 0:
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={"starred_repositories": json.dumps([])},
                )

            log.info(
                f"Retrieved {len(all_starredrepo_models)} Github starred repositories"
            )

            for starred_model in all_starredrepo_models:
                try:
                    starred_schema: stars_domain.GithubStarredRepoOut = stars_domain.converters.convert_github_starred_repo_db_model_to_schema(
                        starred_repo_model=starred_model
                    )
                    starred_repo_out_schemas.append(starred_schema)
                except Exception as exc:
                    msg = f"({type(exc)}) Error converting model to schema. Details: {exc}"
                    log.error(msg)

                    return JSONResponse(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content={"msg": "Internal server error"},
                    )
    except Exception as exc:
        msg = f"({type(exc)}) Error getting all Github stars. Details: {exc}"
        log.error(msg)

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"msg": "Internal server error"},
        )

    if len(starred_repo_out_schemas) == 0:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"msg": "No repositories found"},
        )

    log.info("Start JSON encoding")
    repo_out_dicts: list[dict] = [m.model_dump() for m in starred_repo_out_schemas]

    ## Calculate total number of pages
    total_pages = math.ceil(total_count / page_params.size)

    try:
        return_obj = PagedResponseSchema(
            page=page_params.page,
            size=page_params.size,
            total=total_pages,
            results=starred_repo_out_schemas,
        )
    except Exception as exc:
        msg = f"({type(exc)}) Error creating paged response. Details: {exc}"
        log.error(msg)

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"msg": "Internal server error"},
        )

    return return_obj


@router.get("/count")
def count_stars(request: Request) -> JSONResponse:
    session_pool = db_depends.get_session_pool()

    try:
        with session_pool() as session:
            repo = stars_domain.GithubStarredRepositoryDBRepository(session)

            count = repo.count()

            return JSONResponse(status_code=status.HTTP_200_OK, content={"count": count})
    except Exception as exc:
        msg = f"({type(exc)}) Error counting Github stars. Details: {exc}"
        log.error(msg)

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"msg": "Internal server error"},
        )
        
@router.get("/search/date/created", response_model=None)
def search_by_created_date(request: Request, created_at: str, cardinality: str = "on", page_params: PageParams = Depends()) -> JSONResponse | PagedResponseSchema:
    session_pool = db_depends.get_session_pool()

    try:
        with session_pool() as session:
            ghrepo_repo = stars_domain.GithubStarredRepositoryDBRepository(session)

            starred_repo_out_schemas: list[stars_domain.GithubStarredRepoOut] = []

            starred_repo_models: list[stars_domain.GithubStarredRepositoryModel] = (
                ghrepo_repo.get_by_created_date(created_at=created_at, cardinality=cardinality)
            )
            
            total_count = ghrepo_repo.count()

            if len(starred_repo_models) == 0:
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={"starred_repositories": json.dumps([])},
                )

            log.info(f"Retrieved {len(starred_repo_models)} Github starred repositories")

            for starred_model in starred_repo_models:
                try:
                    starred_schema: stars_domain.GithubStarredRepoOut = stars_domain.converters.convert_github_starred_repo_db_model_to_schema(
                        starred_repo_model=starred_model
                    )
                    starred_repo_out_schemas.append(starred_schema)
                except Exception as exc:
                    msg = f"({type(exc)}) Error converting model to schema. Details: {exc}"
                    log.error(msg)

                    return JSONResponse(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content={"msg": "Internal server error"},
                    )
    except Exception as exc:
        msg = f"({type(exc)}) Error getting all Github stars. Details: {exc}"
        log.error(msg)

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"msg": "Internal server error"},
        )

    if len(starred_repo_out_schemas) == 0:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"msg": "No repositories found"},
        )
        
    return_repos = [repo.model_dump() for repo in starred_repo_out_schemas]
    
    
    ## Calculate total number of pages
    total_pages = math.ceil(total_count / page_params.size)

    try:
        return_obj = PagedResponseSchema(
            page=page_params.page,
            size=page_params.size,
            total=total_pages,
            results=return_repos,
        )
    except Exception as exc:
        msg = f"({type(exc)}) Error creating paged response. Details: {exc}"
        log.error(msg)

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"msg": "Internal server error"},
        )

    return return_obj
