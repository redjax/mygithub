from loguru import logger as log
import json

from mygh.libs import setup, settings
from mygh.controllers import GithubAPIController
from mygh.libs.depends import db_depends
from mygh.libs import db_lib
from mygh.domain.github import stars as stars_domain


def main(api_token: str):
    log.debug("Setting up Github API controller")
    gh_api_controller: GithubAPIController = GithubAPIController(api_token=api_token, cache_ttl=10800)

    with gh_api_controller as gh:
        starred_repos = gh.get_user_stars()

    log.debug(f"Found [{len(starred_repos)}] starred repositories.")

    log.info("Saving repositories to starred.json")
    # with open("starred.json", "w") as f:
    #     _data = json.dumps(starred_repos, indent=4, sort_keys=True, default=str)
    #     f.write(_data)
        
    session_pool = db_depends.get_session_pool()
    
    with session_pool() as session:
        api_response_repo = stars_domain.GithubStarsAPIResponseRepository(session)
        gh_repository_repo = stars_domain.GithubStarredRepositoryDBRepository(session)
        
        db_api_response_model = stars_domain.GithubStarsAPIResponseModel(json_data=starred_repos)
        
        try:
            db_api_response_model = api_response_repo.create(db_api_response_model)
        except Exception as e:
            msg = f"({type(e)}) Unhandled exception saving API response. Details: {e}"
            log.error(msg)            
            raise
        
        log.info(f"Saved API response [{db_api_response_model.id}] to database")
        
        log.info("Extracting repositories and owners from API response")
        for repo_data in starred_repos:
            repo_owner_data = repo_data["owner"]
            
            ## Create owner model
            repo_owner = stars_domain.GithubRepositoryOwnerModel(
                id=repo_owner_data["id"],
                login=repo_owner_data["login"],
                node_id=repo_owner_data["node_id"],
                avatar_url=repo_owner_data["avatar_url"],
                gravatar_id=repo_owner_data.get("gravatar_id"),  # Nullable field
                url=repo_owner_data["url"],
                html_url=repo_owner_data["html_url"],
                followers_url=repo_owner_data["followers_url"],
                following_url=repo_owner_data["following_url"],
                gists_url=repo_owner_data["gists_url"],
                starred_url=repo_owner_data["starred_url"],
                subscriptions_url=repo_owner_data["subscriptions_url"],
                organizations_url=repo_owner_data["organizations_url"],
                repos_url=repo_owner_data["repos_url"],
                events_url=repo_owner_data["events_url"],
                received_events_url=repo_owner_data["received_events_url"],
                type=repo_owner_data["type"],
                user_view_type=repo_owner_data.get("user_view_type", "User"),  # Fallback value
                site_admin=repo_owner_data["site_admin"],
            )
            
            ## Create Repository Model instance
            github_repo = stars_domain.GithubStarredRepositoryModel(
                repo_id=repo_data["id"],
                name=repo_data["name"],
                full_name=repo_data["full_name"],
                description=repo_data["description"],
                html_url=repo_data["html_url"],
                stargazers_count=repo_data["stargazers_count"],
                language=repo_data.get("language"),
                owner=repo_owner
            )
            
            ## Save to database using the repository class
            try:
                saved_repo: stars_domain.GithubStarredRepositoryModel = gh_repository_repo.create_or_get_repo(github_repo, repo_owner)
            except Exception as exc:
                msg = f"({type(exc)}) Unhandled exception saving repository. Details: {exc}"
                log.error(msg)
                raise

            log.info(f"Processed repository: {saved_repo.name} (ID: {saved_repo.repo_id})")
        
                
    log.debug(f"Saved github stars to database")
    


if __name__ == "__main__":
    setup.setup_loguru_logging(
        log_level=settings.LOGGING_SETTINGS.get("LOG_LEVEL", default="INFO"),
        colorize=True,
    )
    setup.setup_database()

    API_KEY = settings.GITHUB_SETTINGS.get("GH_API_TOKEN", default=None)
    log.debug(f"Github API key: {API_KEY}")

    main(api_token=API_KEY)
