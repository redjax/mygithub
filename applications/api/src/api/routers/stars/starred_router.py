from __future__ import annotations

import typing as t
import json

from api import helpers as api_helpers
from api.responses import API_RESPONSE_DICT
from api.pagination import PageParams, PagedResponseSchema

from fastapi import APIRouter, Depends, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse, JSONResponse, Response, StreamingResponse
from loguru import logger as log

from domain.github import stars as stars_domain
from depends import db_depends
import db_lib

import sqlalchemy as sa
import sqlalchemy.orm as so
import sqlalchemy.exc as sa_exc


__all__ = ["router"]

prefix: str = "/stars"

tags: list[str] = ["stars"]

router: APIRouter = APIRouter(prefix=prefix, responses=API_RESPONSE_DICT, tags=tags)


@router.get("/all")
def return_all_stars(request: Request, page_params: PageParams = Depends()) -> JSONResponse:
    session_pool = db_depends.get_session_pool()
    
    starred_repo_out_schemas: list[stars_domain.GithubStarredRepoOut] = []
    
    log.info("Retrieving all Github starred repositories")
    try:
        with session_pool() as session:
            repo = stars_domain.GithubStarredRepositoryDBRepository(session)
            
            all_starredrepo_models: list[stars_domain.GithubStarredRepositoryModel] = repo.get_all()
            
            if len(all_starredrepo_models) == 0:
                return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"starred_repositories": json.dumps([])})
            
            log.info(f"Retrieved {len(all_starredrepo_models)} Github starred repositories")
            
            for starred_model in all_starredrepo_models:
                try:
                    starred_schema: stars_domain.GithubStarredRepoOut = stars_domain.converters.convert_github_starred_repo_db_model_to_schema(starred_repo_model=starred_model)
                    # starred_schema.id = starred_model.id
                    starred_repo_out_schemas.append(starred_schema)
                except Exception as exc:
                    msg = f"({type(exc)}) Error converting model to schema. Details: {exc}"
                    log.error(msg)
                    
                    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"msg": "Internal server error"})
    except Exception as exc:
        msg = f"({type(exc)}) Error getting all Github stars. Details: {exc}"
        log.error(msg)
        
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"msg": "Internal server error"})
    
    if len(starred_repo_out_schemas) == 0:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"msg": "No repositories found"})
    
    log.info(f"Retrieved [{len(starred_repo_out_schemas)}] Github starred repositor{'y' if len(starred_repo_out_schemas) == 1 else 'ies'}")

    # log.info("Start JSON encoding")
    try:
        res_json = jsonable_encoder(starred_repo_out_schemas)
        log.info("End JSON encoding")
    except Exception as exc:
        log.info("End JSON decoding")
        msg = f"({type(exc)}) Error encoding response. Details: {exc}"
        log.error(msg)
        
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"msg": "Internal server error"})

    # log.info("Start return response")
    # return JSONResponse(status_code=status.HTTP_200_OK, content={"starred_repositories": res_json})
    
    return_obj: PagedResponseSchema[stars_domain.GithubStarredRepoOut] = PagedResponseSchema[stars_domain.GithubStarredRepoOut](
        page=page_params.page,
        page_size=page_params.size,
        total=len(starred_repo_out_schemas),
        items=starred_repo_out_schemas,
    )
    
    return return_obj
        
        