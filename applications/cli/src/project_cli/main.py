from __future__ import annotations

import sys
import typing as t

from .subcommands._alembic import alembic_app
from .subcommands.api import api_app
from .subcommands.db import db_app
from .subcommands.github import gh_app

from cyclopts import App, Group, Parameter
from loguru import logger as log

app = App(name="mygithub", help="CLI for MyGithub Python app.")

app.meta.group_parameters = Group("Session Parameters", sort_key=0)

MOUNT_SUB_CLIS: list = [alembic_app, db_app, gh_app, api_app]

## Mount sub-CLIs
for sub_cli in MOUNT_SUB_CLIS:
    app.command(sub_cli)
    
@app.meta.default
def cli_launcher(
    *tokens: t.Annotated[str, Parameter(show=False, allow_leading_hyphen=True)],
    debug: bool = False,
):
    """CLI entrypoint.

    Params:
        debug (bool): If `True`, enables debug logging.
    """
    # log.remove(0)

    if debug:
        log.add(
            sys.stderr,
            format="{time:YYYY-MM-DD HH:mm:ss} | [{level}] | {name}.{function}:{line} |> {message}",
            level="DEBUG",
        )

        log.debug("CLI debugging enabled.")
    else:
        log.add(
            sys.stderr,
            format="{time:YYYY-MM-DD HH:mm:ss} [{level}] : {message}",
            level="INFO",
        )

    app(tokens)


if __name__ == "__main__":
    app()
