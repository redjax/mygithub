from __future__ import annotations

from cyclopts import App
from loguru import logger as log
from mygh.libs.settings.logging_settings import LOGGING_SETTINGS
from  mygh.libs import setup
import mygh.cli


def start_cli(app: App):
    try:
        app.meta()
    except Exception as exc:
        msg = f"({type(exc)}) error"
        log.error(msg)

        raise exc


if __name__ == "__main__":
    setup.setup_loguru_logging(log_level="ERROR", log_fmt="basic", colorize=True)
    start_cli(app=mygh.cli.cli_app)
