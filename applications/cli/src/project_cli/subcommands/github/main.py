from __future__ import annotations

from pathlib import Path
import typing as t

from .gh_stars import gh_stars_app

from cyclopts import App, Group, Parameter
from loguru import logger as log

gh_app = App(name="gh", help="Github operations")

MOUNT_SUB_CLIS = [gh_stars_app]

for sub_cli in MOUNT_SUB_CLIS:
    gh_app.command(sub_cli)