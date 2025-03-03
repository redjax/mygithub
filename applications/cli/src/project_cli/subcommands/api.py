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

api_app =  App("api", help="API operations")

@api_app.command(name="run")
def run_api_server():
    uvicorn_settings = UvicornSettings()
    log.debug(f"Uvicorn settings class: {uvicorn_settings}")
    
    log.info("Initializing custom Uvicorn server object")
    uvicorn_server: UvicornCustomServer = initialize_custom_server(uvicorn_settings=uvicorn_settings, uvicorn_log_level=settings.UVICORN_SETTINGS.get("UVICORN_LOG_LEVEL"))
    
    log.info("Starting uvicorn server")
    try:
        start_api.run_uvicorn_server(uvicorn_server=uvicorn_server)
    except Exception as exc:
        msg = f"({type(exc)}) Error starting Uvicorn server. Details: {exc}"
        log.error(msg)
        
        raise exc