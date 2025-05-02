import schedule
import gh_client
from settings import GITHUB_SETTINGS
from loguru import logger as log

__all__ = ["sched_every_15m_gh_user_stars"]


def sched_every_15m_gh_user_stars(
    api_token: str,
    save_db: bool = False,
    save_json: bool = False,
    json_file: str = "starred.json",
    use_cache: bool = False,
    cache_ttl: int = 900,
):
    if not api_token or api_token == "":
        raise ValueError(
            "Missing Github API key. Check your GH_API_KEY environment variable"
        )

    job_details = {
        "func": gh_client.get_user_stars,
        "kwargs": {
            "api_token": api_token,
            "save_db": save_db,
            "save_json": save_json,
            "json_file": json_file,
            "use_cache": use_cache,
            "cache_ttl": cache_ttl,
        },
    }

    schedule.every().hour.at(":15").do(job_details["func"], **job_details["kwargs"])

    log.info("Requesting Github stars every 15 minutes")
    try:
        while True:
            schedule.run_pending()
    except KeyboardInterrupt:
        log.error("Interrupted by user")
        return
    except Exception as exc:
        log.error(f"Error requesting user's Github stars. Details: {exc}")
        raise
