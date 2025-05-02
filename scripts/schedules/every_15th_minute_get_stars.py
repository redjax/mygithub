from scheduling import lib_schedule
import setup
from settings import GITHUB_SETTINGS, LOGGING_SETTINGS
from loguru import logger as log

if __name__ == "__main__":
    log_level = LOGGING_SETTINGS.get("LOG_LEVEL", "INFO").upper()
    setup.setup_loguru_logging(log_level=log_level, colorize=True)
    log.debug("DEBUG logging enabled.")

    api_token = GITHUB_SETTINGS.get("GH_API_TOKEN")

    if not api_token or api_token == "":
        log.error(f"API token is empty.")
        exit(1)

    lib_schedule.sched_every_15m_gh_user_stars(
        api_token=api_token,
        save_db=True,
        save_json=True,
        json_file="my_stars.json",
        use_cache=True,
        cache_ttl=900,
    )
