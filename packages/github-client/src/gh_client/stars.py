from __future__ import annotations

import json
from pathlib import Path
import typing as t

from controllers import GithubAPIController
from depends import db_depends
from domain.github import stars as stars_domain
from loguru import logger as log
import settings


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


# def save_github_stars(
#     starred_repos: list[dict],
# ) -> list[stars_domain.GithubStarredRepositoryModel]:
#     session_pool = db_depends.get_session_pool()

#     saved_repos: list[stars_domain.GithubStarredRepositoryModel] = []
#     existing_repos: list[stars_domain.GithubStarredRepositoryModel] | None = []

#     with session_pool() as session:
#         api_response_repo = stars_domain.GithubStarsAPIResponseRepository(session)
#         gh_repository_repo = stars_domain.GithubStarredRepositoryDBRepository(session)

#         db_api_response_model = stars_domain.GithubStarsAPIResponseModel(
#             json_data=starred_repos
#         )

#         log.debug("Saving API response to database")
#         try:
#             db_api_response_model = api_response_repo.create(db_api_response_model)
#         except Exception as e:
#             msg = f"({type(e)}) Unhandled exception saving API response. Details: {e}"
#             log.error(msg)
#             raise

#         log.debug(f"Saved API response to database [response_id: {db_api_response_model.id}]")

#         log.debug("Extracting repositories and owners from API response")
#         for repo_data in starred_repos:
#             existing_repo: stars_domain.GithubStarredRepositoryModel | None = gh_repository_repo.get_by_gh_id(id=repo_data["id"])
#             print(f"Existing repo ({type(existing_repo)}, ID: {existing_repo.repo_id or None}): {existing_repo}")
#             # existing_owner: stars_domain.GithubRepositoryOwnerModel | None = gh_o
#             if existing_repo is not None:
#                 print(f"Repo {existing_repo.name} already exists in database [repo_id: {existing_repo.repo_id}]")
#                 log.debug(f"Repo already exists in database [repo_id: {existing_repo.repo_id}]")
#                 existing_repos.append(existing_repo)

#                 continue
            
#             log.debug(f"Repo does not exist in database [repo_id: {repo_data['id']}]")
#             repo_owner_data = repo_data["owner"]

#             ## Create owner model
#             repo_owner_schema: stars_domain.GithubRepositoryOwnerIn = (
#                 stars_domain.GithubRepositoryOwnerIn.model_validate(repo_owner_data)
#             )
#             repo_owner: stars_domain.GithubRepositoryOwnerModel = stars_domain.converters.convert_github_repository_owner_schema_to_db_model(
#                 owner=repo_owner_schema
#             )

#             ## Create Repository Model instance
#             github_repo_schema: stars_domain.GithubStarredRepoIn = (
#                 stars_domain.GithubStarredRepoIn.model_validate(repo_data)
#             )
#             github_repo: stars_domain.GithubStarredRepositoryModel = (
#                 stars_domain.converters.convert_github_starred_repo_schema_to_db_model(
#                     github_repo_schema
#                 )
#             )

#             ## Save to database using the repository class
#             try:
#                 saved_repo: stars_domain.GithubStarredRepositoryModel = (
#                     gh_repository_repo.create_or_get_repo(github_repo, repo_owner)
#                 )
#                 saved_repos.append(saved_repo)
#             except sa_exc.IntegrityError as exc:
#                 msg = f"({type(exc)}) Repository '{repo_data['name']}' already exists in the database. Skipping save."
#                 log.debug(msg)
                
#                 continue
#             except Exception as exc:
#                 msg = f"({type(exc)}) Unhandled exception saving repository. Details: {exc}"
#                 log.error(msg)
#                 raise

#             log.debug(
#                 f"Processed repository: {saved_repo.name} (ID: {saved_repo.repo_id})"
#             )

#     ## Join saved_repos and existing
#     saved_repos = saved_repos + existing_repos
    
#     return saved_repos

def save_github_stars(
    starred_repos: list[dict],
) -> list[stars_domain.GithubStarredRepositoryModel]:
    session_pool = db_depends.get_session_pool()

    existing_repos: list[stars_domain.GithubStarredRepositoryModel] | None =  []
    saved_repos: list[stars_domain.GithubStarredRepositoryModel] = []

    with session_pool() as session:
        api_response_repo = stars_domain.GithubStarsAPIResponseRepository(session)
        gh_repository_repo = stars_domain.GithubStarredRepositoryDBRepository(session)

        db_api_response_model = stars_domain.GithubStarsAPIResponseModel(json_data=starred_repos)

        log.debug("Saving API response to database")
        try:
            db_api_response_model = api_response_repo.create(db_api_response_model)
        except Exception as e:
            log.error(f"({type(e)}) Unhandled exception saving API response. Details: {e}")
            raise

        log.debug(f"Saved API response to database [response_id: {db_api_response_model.id}]")

        # Extract all repo IDs from the API response
        # repo_ids = {repo_data["id"] for repo_data in starred_repos}
        node_ids = {repo_data["node_id"] for repo_data in starred_repos}
        
        existing_node_ids = set()
        
        # for _id in repo_ids:
        for _id in node_ids:
            # repo = gh_repository_repo.get_by_gh_id(id=_id)
            repo = gh_repository_repo.get_by_node_id(node_id=_id)

            if repo:
                existing_node_ids.add(_id)

        log.debug(f"Found {len(existing_node_ids)} existing repositories in the database.")
        
        if len(existing_node_ids) == 0:
            log.info("No existing repositories found, committing all")
        else:
            log.debug(f"Retrieving [{len(existing_node_ids)}] repositor(y/ies) from database")
            
            for _existing_node_id in existing_node_ids:
                repo = gh_repository_repo.get_by_node_id(node_id=_existing_node_id)
                existing_repos.append(repo)

        ## Filter out repositories that already exist
        new_repos_data = [
            repo_data for repo_data in starred_repos if repo_data["node_id"] not in existing_node_ids
        ] or []
        
        if len(new_repos_data) == 0:
            log.debug("No new repositories found.")
            
            return existing_repos

        log.info(f"Processing {len(new_repos_data)} new repositories.")

        for repo_data in new_repos_data:
            repo_owner_data = repo_data["owner"]

            # Create owner model
            repo_owner_schema = stars_domain.GithubRepositoryOwnerIn.model_validate(repo_owner_data)
            repo_owner = stars_domain.converters.convert_github_repository_owner_schema_to_db_model(
                owner=repo_owner_schema
            )

            # Create Repository Model instance
            github_repo_schema = stars_domain.GithubStarredRepoIn.model_validate(repo_data)
            github_repo = stars_domain.converters.convert_github_starred_repo_schema_to_db_model(
                github_repo_schema
            )

            # Save to database using repository class
            try:
                saved_repo = gh_repository_repo.create_or_get_repo(github_repo, repo_owner)
                saved_repos.append(saved_repo)
            except sa_exc.IntegrityError as exc:
                log.debug(f"IntegrityError: Repository '{repo_data['name']}' already exists. Skipping save.")
                session.rollback()
                continue
            except Exception as exc:
                log.error(f"({type(exc)}) Unhandled exception saving repository. Details: {exc}")
                raise

            log.debug(f"Saved repository: {saved_repo.name} (ID: {saved_repo.repo_id})")

    return saved_repos
