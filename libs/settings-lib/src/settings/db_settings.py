from __future__ import annotations

from dynaconf import Dynaconf # type: ignore
from loguru import logger as log

## Database settings loaded with dynaconf
DB_SETTINGS: Dynaconf = Dynaconf(
    environments=True,
    envvar_prefix="DB",
    settings_files=["settings.toml", ".secrets.toml"],
)
