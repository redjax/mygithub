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
        repo = stars_domain.GithubStarsAPIResponseRepository(session)
        db_model = stars_domain.GithubStarsAPIResponseModel(json_data=starred_repos)
                
        db_model = repo.create(db_model)
        
        log.info(f"Saved [{db_model.id}] to database")
    
    log.debug(f"Saved github stars to database")
    
    starred_repos_response = stars_domain.GithubStarsAPIResponseOut.model_validate(db_model.__dict__)
    log.info(starred_repos_response)
    


if __name__ == "__main__":
    setup.setup_loguru_logging(
        log_level=settings.LOGGING_SETTINGS.get("LOG_LEVEL", default="INFO"),
        colorize=True,
    )
    setup.setup_database()

    API_KEY = settings.GITHUB_SETTINGS.get("GH_API_TOKEN", default=None)
    log.debug(f"Github API key: {API_KEY}")

    main(api_token=API_KEY)
