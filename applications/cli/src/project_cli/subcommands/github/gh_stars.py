from __future__ import annotations

from pathlib import Path
import typing as t

from packages.controllers.src.controllers import GithubAPIController

from cyclopts import App, Group, Parameter
from domain.github import stars as stars_domain
import gh_client
from loguru import logger as log
import settings
import sqlalchemy as sa
import sqlalchemy.exc as sa_exc
import sqlalchemy.orm as so

gh_stars_app = App(name="stars", help="Github starred repositories")


@gh_stars_app.command(
    name="get", help="Get starred repositories associated with Github PAT."
)
def get_user_stars(
    api_token: t.Annotated[str, Parameter("api-token", show_default=True)] = None,
    save: t.Annotated[bool, Parameter("save", show_default=True)] = False,
    use_cache: t.Annotated[bool, Parameter("use-cache", show_default=True)] = True,
    cache_ttl: t.Annotated[int, Parameter("cache-ttl", show_default=True)] = 900,
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
        starred_repos: list[dict] = gh_client.get_starred_repos(
            api_token=api_token, use_cache=use_cache, cache_ttl=cache_ttl
        )
    except Exception as exc:
        msg = f"({type(exc)}) Error getting user's starred repositories. Details: {exc}"
        log.error(msg)

        return

    log.info(f"Requested [{len(starred_repos)}] starred repo(s) from Github")

    if save:
        log.info("Saving requested repositories to database")

        try:
            saved_stars = gh_client.save_github_stars(starred_repos=starred_repos)
            log.success(f"Saved starred repositories to database")
        except Exception as exc:
            msg = f"({type(exc)}) Error saving starred repositories to database. Details: {exc}"
            log.error(msg)

            return
