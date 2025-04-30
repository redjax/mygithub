from __future__ import annotations

import json
from pathlib import Path
import typing as t

from cli_spinners import CustomSpinner
from controllers import GithubAPIController
from depends import db_depends
from domain.github import stars as stars_domain
from loguru import logger as log
import settings
import sqlalchemy.exc as sa_exc


__all__ = ["get_starred_repos", "save_github_stars", "get_user_stars"]


def get_starred_repos(
    api_token: str = settings.GITHUB_SETTINGS.get("GH_API_TOKEN", default=None),
    use_cache: bool = False,
    cache_ttl: int = 900,
):
    gh_api_controller: GithubAPIController = GithubAPIController(
        api_token=api_token, use_cache=use_cache, cache_ttl=cache_ttl
    )

    try:
        with gh_api_controller as gh:
            starred_repos = gh.get_user_stars()
        return starred_repos
    except Exception as exc:
        msg = f"({type(exc)}) Unhandled exception getting user's starred repositories. Details: {exc}"
        log.error(msg)
        raise


def save_github_stars(
    starred_repos: list[dict],
) -> list[stars_domain.GithubStarredRepositoryModel]:
    session_pool = db_depends.get_session_pool()

    existing_repos: list[stars_domain.GithubStarredRepositoryModel] | None = []
    saved_repos: list[stars_domain.GithubStarredRepositoryModel] = []
    existing_repos: list[stars_domain.GithubStarredRepositoryModel] | None = []

    with session_pool() as session:
        ## Initialize DB repository classes
        api_response_repo: stars_domain.GithubStarsAPIResponseRepository = (
            stars_domain.GithubStarsAPIResponseRepository(session)
        )
        gh_repository_repo: stars_domain.GithubStarredRepositoryDBRepository = (
            stars_domain.GithubStarredRepositoryDBRepository(session)
        )

        ## Create DB entity for API response
        db_api_response_model: stars_domain.GithubStarsAPIResponseModel = (
            stars_domain.GithubStarsAPIResponseModel(json_data=starred_repos)
        )

        log.debug("Saving API response to database")
        try:
            db_api_response_model: stars_domain.GithubStarsAPIResponseModel = (
                api_response_repo.create(db_api_response_model)
            )
        except Exception as e:
            log.error(
                f"({type(e)}) Unhandled exception saving API response. Details: {e}"
            )
            raise

        log.debug(
            f"Saved API response to database [response_id: {db_api_response_model.id}]"
        )

        ## Extract all repo IDs from the API response
        node_ids: set[str] = {repo_data["node_id"] for repo_data in starred_repos}

        ## Initialize set to hold existing repository IDs
        #  These IDs come from Github
        existing_node_ids: set[str] = set()

        ## Loop over nodes and check for existence in DB
        for _id in node_ids:
            ## Lookup repo by node_id
            repo: stars_domain.GithubStarredRepositoryModel = (
                gh_repository_repo.get_by_node_id(node_id=_id)
            )

            if repo:
                ## Repo exists, add to set
                existing_node_ids.add(_id)

        log.debug(
            f"Found {len(existing_node_ids)} existing repositories in the database."
        )

        if len(existing_node_ids) == 0:
            log.info("No existing repositories found, committing all")
        else:
            ## 1 or more repos exist in database already
            log.debug(
                f"Retrieving [{len(existing_node_ids)}] repositor(y/ies) from database"
            )

            ## Retrieve existing entity from the database
            for _existing_node_id in existing_node_ids:
                repo: stars_domain.GithubStarredRepositoryModel = (
                    gh_repository_repo.get_by_node_id(node_id=_existing_node_id)
                )
                existing_repos.append(repo)

        ## Filter out repositories that already exist
        new_repos_data: list[dict] = [
            repo_data
            for repo_data in starred_repos
            if repo_data["node_id"] not in existing_node_ids
        ] or []

        if len(new_repos_data) == 0:
            log.debug("No new repositories found.")

            ## All repos already exist in the database, return the existing entities
            return existing_repos

        log.info(f"Processing {len(new_repos_data)} new repositories.")

        ## Save new repositories
        for repo_data in new_repos_data:
            repo_owner_data: str = repo_data["owner"]

            ## Create owner schema
            try:
                repo_owner_schema: stars_domain.GithubRepositoryOwnerIn = (
                    stars_domain.GithubRepositoryOwnerIn.model_validate(repo_owner_data)
                )
            except Exception as e:
                msg = f"({type(exc)}) Error validating repository owner schema. Details: {e}"
                log.error(msg)

                raise

            ## Convert owner schema to DB model
            try:
                repo_owner: stars_domain.GithubRepositoryOwnerModel = (
                    stars_domain.converters.convert_github_repository_owner_schema_to_db_model(
                        owner=repo_owner_schema
                    )
                )
            except Exception as exc:
                msg = f"({type(exc)}) Error converting repository owner schema to DB model. Details: {exc}"
                log.error(msg)

                raise

            ## Create starred repository model instance
            try:
                github_repo_schema: stars_domain.GithubStarredRepoIn = (
                    stars_domain.GithubStarredRepoIn.model_validate(repo_data)
                )
            except Exception as e:
                msg = f"({type(exc)}) Error validating starred repository schema. Details: {e}"
                log.error(msg)

                raise

            ## Convert starred repository schema to DB model
            try:
                github_repo: stars_domain.GithubStarredRepositoryModel = (
                    stars_domain.converters.convert_github_starred_repo_schema_to_db_model(
                        github_repo_schema
                    )
                )
            except Exception as exc:
                msg = f"({type(exc)}) Error converting starred repository schema to DB model. Details: {exc}"
                log.error(msg)

                raise

            # Save to database using repository class
            try:
                saved_repo: stars_domain.GithubStarredRepositoryModel = (
                    gh_repository_repo.create_or_get_repo(github_repo, repo_owner)
                )
                saved_repos.append(saved_repo)

            except sa_exc.IntegrityError as exc:
                log.debug(
                    f"IntegrityError: Repository '{repo_data['name']}' already exists. Skipping save."
                )
                session.rollback()

                continue

            except Exception as exc:
                log.error(
                    f"({type(exc)}) Unhandled exception saving repository. Details: {exc}"
                )
                raise

            log.debug(f"Saved repository: {saved_repo.name} (ID: {saved_repo.repo_id})")

    ## Join saved_repos and existing
    saved_repos: list[stars_domain.GithubStarredRepositoryModel] = (
        saved_repos + existing_repos
    )

    return saved_repos


def get_user_stars(
    api_token: str,
    save_db: bool,
    save_json: bool,
    json_file: str = "starred.json",
    use_cache: bool = True,
    cache_ttl: int = 3600,
):
    """Get starred repositories associated with Github PAT.

    Description:
        Joins the get_starred_repos() and save_github_stars() functions into a single call.

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
        with CustomSpinner("Getting user's starred repositories...") as spinner:
            starred_repos: list[dict] = get_starred_repos(
                api_token=api_token, use_cache=use_cache, cache_ttl=cache_ttl
            )
    except Exception as exc:
        msg = f"({type(exc)}) Error getting user's starred repositories. Details: {exc}"
        log.error(msg)

        return

    log.info(f"Requested [{len(starred_repos)}] starred repo(s) from Github")

    if save_db:
        log.info("Saving requested repositories to database")

        log.info(f"Saving [{len(starred_repos)}] starred repositories to database...")
        try:
            with CustomSpinner(
                f"Saving [{len(starred_repos)}] starred repositories to database..."
            ):
                saved_stars = save_github_stars(starred_repos=starred_repos)
                log.success(f"Saved starred repositories to database")
        except Exception as exc:
            msg = f"({type(exc)}) Error saving starred repositories to database. Details: {exc}"
            log.error(msg)

            return

    if save_json:
        if json_file is None:
            json_file = "starred.json"

        json_file: Path = Path(json_file)

        if json_file.exists():
            log.warning(
                f"JSON file '{json_file}' already exists and will be overwritten"
            )

        try:
            json_data = json.dumps(starred_repos, indent=4, default=str, sort_keys=True)
            with open(json_file, "w") as f:
                f.write(json_data)

            log.success(f"Saved starred repositories to {json_file}")
        except Exception as exc:
            msg = f"({type(exc)}) Error saving starred repositories to {json_file}. Details: {exc}"
            log.error(msg)

            return
