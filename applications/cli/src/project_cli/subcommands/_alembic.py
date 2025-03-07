from __future__ import annotations

import argparse
from contextlib import AbstractContextManager
import logging
from pathlib import Path
import typing as t

from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory
from project_cli._controller import AlembicController

from cyclopts import App, Group, Parameter
from loguru import logger as log

__all__ = ["alembic_app", "create_migration", "upgrade_db", "downgrade_db"]

alembic_app: App = App(name="alembic", help="CLI for Alembic operations.")


@alembic_app.command(name="do-migration", help="Generate a new migration file.")
def create_migration(
    message: t.Annotated[
        str,
        Parameter(
            "message",
            show_default=True,
            help="The message for the Alembic revision.",
        ),
    ] = "autogenerated migration",
    do_upgrade: t.Annotated[
        bool,
        Parameter(
            name="do-upgrade",
            show_default=True,
            help="Upgrade the database after creating the migration.",
        ),
    ] = False,
    dry_run: t.Annotated[
        bool,
        Parameter(
            name="dry-run",
            show_default=True,
            help="Simulate migration creation.",
        ),
    ] = False,
):
    try:
        with AlembicController(do_upgrade=do_upgrade, dry_run=dry_run) as ac:
            ac.create_migration(message=message)
    except Exception as exc:
        msg = f"({type(exc)}) Error creating migration: {exc}"
        log.error(msg)
        raise exc


@alembic_app.command(
    name="upgrade", help="Upgrade to a specific revision. Default is 'head'."
)
def upgrade_db(
    revision: t.Annotated[
        str,
        Parameter(
            name="revision",
            show_default=True,
            help="The revision hash to upgrade to, or 'head' to upgrade to the latest revision.",
        ),
    ] = "head",
    dry_run: t.Annotated[
        bool,
        Parameter(
            name="dry-run",
            show_default=True,
            help="Simulate migration creation.",
        ),
    ] = False,
):
    try:
        with AlembicController(dry_run=dry_run) as ac:
            ac.upgrade(revision=revision)
    except Exception as exc:
        msg = f"({type(exc)}) Error upgrading to revision '{revision}'. Details: {exc}"
        log.error(msg)
        raise exc


@alembic_app.command(
    name="downgrade",
    help="Downgrade to a specific revision, or a number of revisions back with an negative integer, i.e. -3. Default is '-1'.",
)
def downgrade_db(
    revision: t.Annotated[
        str,
        Parameter(
            name="revision",
            show_default=True,
            help="The revision hash to downgrade to, or a negative integer (i.e. '-3') to revert.",
        ),
    ] = "-1",
    dry_run: t.Annotated[
        bool,
        Parameter(
            name="dry-run",
            show_default=True,
            help="Simulate migration creation.",
        ),
    ] = False,
):
    try:
        with AlembicController(dry_run=dry_run) as ac:
            ac.downgrade(revision=revision)
    except Exception as exc:
        msg = (
            f"({type(exc)}) Error downgrading to revision '{revision}'. Details: {exc}"
        )
        log.error(msg)
        raise exc
