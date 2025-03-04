from __future__ import annotations

import typing as t

from api import (
    UvicornCustomServer,
    UvicornSettings,
    initialize_custom_server,
    start_api,
)
from cyclopts import App, Group, Parameter
from loguru import logger as log
import settings

__all__ = ["run_api_server", "api_app"]

api_app = App("api", help="API operations")

@api_app.command(name="run")
def run_api_server(
    host: t.Annotated[
        str,
        Parameter(
            "--host", show_default=True, help="The host address/FQDN for the server."
        ),
    ] = "0.0.0.0",
    port: t.Annotated[
        int,
        Parameter(
            "--port", show_default=True, help="The port the server should run on."
        ),
    ] = 8000,
    reload: t.Annotated[
        bool,
        Parameter(
            "--reload", show_default=True, help="Reload when changes are detected."
        ),
    ] = False,
    log_level: t.Annotated[
        str,
        Parameter(
            "--log-level",
            show_default=True,
            show_choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            help="The log level for the Uvicorn server.",
        ),
    ] = "INFO",
) -> None:
    log_level: str = log_level.upper()
    
    if reload:
        log.info("Enabling Uvicorn server reload")

    uvicorn_settings = UvicornSettings(host=host, port=port, reload=reload, log_level=log_level)
    log.debug(f"Uvicorn settings class: {uvicorn_settings}")

    log.info("Initializing custom Uvicorn server object")
    uvicorn_server: UvicornCustomServer = initialize_custom_server(
        uvicorn_settings=uvicorn_settings,
        uvicorn_log_level=settings.UVICORN_SETTINGS.get("UVICORN_LOG_LEVEL"),
    )

    try:
        start_api.run_uvicorn_server(uvicorn_server=uvicorn_server)
    except Exception as exc:
        msg = f"({type(exc)}) Error starting Uvicorn server. Details: {exc}"
        log.error(msg)

        raise exc
