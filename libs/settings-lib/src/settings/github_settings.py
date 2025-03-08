from __future__ import annotations

from dynaconf import Dynaconf # type: ignore

GITHUB_SETTINGS = Dynaconf(
    environments=True,
    envvar_prefix="GH",
    settings_files=["settings.toml", ".secrets.toml"],
)
