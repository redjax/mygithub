from __future__ import annotations

import json
from pathlib import Path
import typing as t

import mygh.client
from mygh.controllers import GithubAPIController
from mygh.domain.github import stars as stars_domain
from mygh.libs import db_lib, settings, setup
from mygh.libs.depends import db_depends

from loguru import logger as log

def main(api_token: str, save_json: bool = False, json_file: t.Union[str, Path] = "starred.json"):
    log.debug("Setting up Github API controller")
    gh_api_controller: GithubAPIController = GithubAPIController(api_token=api_token, cache_ttl=10800)

    with gh_api_controller as gh:
        starred_repos = gh.get_user_stars()

    log.debug(f"Found [{len(starred_repos)}] starred repositories.")

    log.info("Saving repositories to starred.json")
    with open(str(json_file), "w") as f:
        _data = json.dumps(starred_repos, indent=4, sort_keys=True, default=str)
        f.write(_data)

    try:
        saved_stars = mygh.client.save_github_stars(starred_repos=starred_repos)
        log.debug(f"Saved [{len(saved_stars)}] github stars to database")
    except Exception as exc:
        msg = f"({type(exc)}) Error saving github stars to database. Details: {exc}"
        log.error(msg)
        
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
