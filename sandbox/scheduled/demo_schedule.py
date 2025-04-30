import time
from loguru import logger as log
from settings import LOGGING_SETTINGS
import setup
import schedule
import settings
from project_cli.subcommands import github as gh


def job(
    api_token: str,
    save_db: bool,
    save_json: bool = False,
    json_file: str | None = None,
    use_cache: bool = False,
    cache_ttl: int = 3600,
):
    try:
        gh_stars_job = gh.get_user_stars(
            api_token=api_token,
            save_db=save_db,
            save_json=save_json,
            json_file=json_file,
            use_cache=use_cache,
            cache_ttl=cache_ttl,
        )
    except Exception as exc:
        log.error(f"({type(exc)}) Error during scheduled job: {exc}")
        raise exc


def main(job_tag: str = "hourly"):
    gh_settings = settings.get_namespace("github")
    api_token = gh_settings.get("GH_API_TOKEN")
    log.debug(f"Github API token: {api_token}")

    schedule.every().hour.at(":00").do(
        job,
        api_token=api_token,
        save_db=True,
        save_json=False,
        json_file=None,
        use_cache=True,
        cache_ttl=900,
    ).tag("hourly")

    schedule.every().minute.at(":00").do(
        job,
        api_token=api_token,
        save_db=True,
        save_json=False,
        json_file=None,
        use_cache=True,
        cache_ttl=900,
    ).tag("minutely")

    log.info(f"Starting check for starred Github repositories [job tag: {job_tag}]")
    while True:
        ## Only run jobs with the "minutely" tag that are pending
        for scheduled_job in schedule.get_jobs():
            if (
                job_tag in getattr(scheduled_job, "tags", set())
                and scheduled_job.should_run
            ):
                scheduled_job.run()


if __name__ == "__main__":
    log_level = LOGGING_SETTINGS.get("LOG_LEVEL", "INFO")
    setup.setup_loguru_logging(
        log_level=log_level,
        log_fmt="detailed" if log_level == "DEBUG" else "basic",
        colorize=True,
    )
    log.debug("DEBUG logging enabled")

    try:
        main()
    except Exception as exc:
        log.error(f"({type(exc)}) Error during scheduled job: {exc}")
        exit(1)
