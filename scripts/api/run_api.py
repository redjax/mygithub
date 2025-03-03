from __future__ import annotations

from api import (
    UvicornCustomServer,
    UvicornSettings,
    initialize_custom_server,
    start_api,
)
from loguru import logger as log
import settings
import setup

def main():
    log.debug(f"FastAPI settings: {settings.FASTAPI_SETTINGS.as_dict()}")
    log.debug(f"Uvicorn settings: {settings.UVICORN_SETTINGS.as_dict()}")
    
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
    

if __name__ == "__main__":
    setup.setup_loguru_logging(log_level=settings.LOGGING_SETTINGS.get("LOG_LEVEL", default="INFO"))
    
    log.info(f"Start FastAPI app sandbox")
    main()