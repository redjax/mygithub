from __future__ import annotations

import json
from pathlib import Path
import typing as t

from cli_spinners import CustomSpinner
from controllers import GithubAPIController
from cyclopts import App, Group, Parameter
from domain.github import stars as stars_domain
import gh_client
from loguru import logger as log
import settings
import sqlalchemy as sa
import sqlalchemy.exc as sa_exc
import sqlalchemy.orm as so

__all__ = ["gh_stars_app", "get_user_stars"]

gh_stars_app = App(name="stars", help="Github starred repositories")


@gh_stars_app.command(
    name="get", help="Get starred repositories associated with Github PAT."
)
def get_user_stars(
    api_token: t.Annotated[
        str,
        Parameter(
            "api-token",
            show_default=True,
            help="The Github PAT to use with the API. If None/empty, will try to load from the environment.",
        ),
    ] = None,
    save_db: t.Annotated[
        bool,
        Parameter(
            "save-db", show_default=True, help="Save the results to the database."
        ),
    ] = False,
    save_json: t.Annotated[
        bool,
        Parameter(
            "save-json", show_default=True, help="Save the results to a json file."
        ),
    ] = False,
    json_file: (
        t.Annotated[
            str,
            Parameter(
                "json-file", show_default=True, help="The file to save the results to."
            ),
        ]
        | None
    ) = "starred.json",
    use_cache: t.Annotated[bool, Parameter("use-cache", show_default=True)] = True,
    cache_ttl: t.Annotated[int, Parameter("cache-ttl", show_default=True)] = 3600,
):
    """Get starred repositories associated with Github PAT.

    Params:
        api_token (str): The Github PAT to use with the API. If not provided, will look for a value in your config/.secrets.local.toml, or set the GH_API_TOKEN environment variable.
        use_cache (bool): (default: True) Use cached data if available.
        cache_ttl (int): (default: 900) Time to live for cached data.
    """
    if api_token is None:
        api_token = settings.GITHUB_SETTINGS.get("GH_API_TOKEN")
        if api_token is None:
            raise ValueError(
                "Missing a Github PAT to use with the API. Please set a value in your config/.secrets.local.toml, or set the GH_API_TOKEN environment variable."
            )

    try:
        gh_client.get_user_stars(
            api_token=api_token,
            save_db=save_db,
            save_json=save_json,
            json_file=json_file,
            use_cache=use_cache,
            cache_ttl=cache_ttl,
        )
    except Exception as exc:
        log.error(
            f"({type(exc)}) Error getting user's starred repositories. Details: {exc}"
        )
        raise exc
