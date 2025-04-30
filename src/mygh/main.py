from __future__ import annotations

import json
from pathlib import Path
import typing as t

from controllers import GithubAPIController
import db_lib
from depends import db_depends
from domain.github import stars as stars_domain
import gh_client
from loguru import logger as log
import settings
import setup

__all__ = ["main"]


def main(
    api_token: str,
    save_json: bool = False,
    json_file: t.Union[str, Path] = "starred.json",
):
    try:
        gh_client.get_user_stars(
            api_token=api_token,
            save_json=True,
            json_file="starred.json",
            save_db=True,
            use_cache=True,
            cache_ttl=900,
        )
    except Exception as exc:
        log.error(
            f"({type(exc)}) Error requesting & saving user's starred repos. Details: {exc}"
        )
        raise


if __name__ == "__main__":
    setup.setup_loguru_logging(
        log_level=settings.LOGGING_SETTINGS.get("LOG_LEVEL", default="INFO"),
        colorize=True,
    )
    setup.setup_database()

    API_KEY = settings.GITHUB_SETTINGS.get("GH_API_TOKEN", default=None)
    log.debug(f"Github API key: {API_KEY}")

    main(api_token=API_KEY)
