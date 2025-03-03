from __future__ import annotations

import argparse
from contextlib import AbstractContextManager
import logging
from pathlib import Path
import typing as t

from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory

from loguru import logger as log


class AlembicController(AbstractContextManager):
    """Context manager for Alembic operations.

    Params:
        alembic_ini_path (str | Path, optional): Path to the Alembic configuration file. Defaults to "alembic.ini".

    Attributes:
        cfg_file (str): Path to the Alembic configuration file.
        config (Config | None): Alembic configuration object.
        log (logging.Logger | None): Logger for the class.

    Example:
        with AlembicController() as ac:
            ac.upgrade()
            ac.create_migration()

    Raises:
        Exception: If an error occurs during Alembic operations.

    """

    def __init__(
        self,
        alembic_ini_path: t.Union[str, Path] = "alembic.ini",
        dry_run: bool = False,
        do_upgrade: bool = False,
    ):
        ## Path to the Alembic configuration file
        self.cfg_file: str = str(alembic_ini_path)

        ## Dry run flag
        self.dry_run: bool = dry_run

        ## Do upgrade flag
        self.do_upgrade: bool = do_upgrade

        ## Alembic configuration object
        self.config: Config | None = None

        ## Logger for the class
        log: logging.Logger | None = None

    def __enter__(self) -> t.Self:
        ## Initialize Alembic configuration object
        self.config = Config(self.cfg_file)

        return self

    def __exit__(self, exc_type, exc_val, traceback) -> t.Literal[False] | None:
        if exc_val:
            log.error(f"({exc_type}) {exc_val}")

            if traceback:
                log.error(f"Traceback: {traceback}")

            return False

        return True

    def __repr__(self) -> str:
        return f"AlembicController(alembic_ini_path={self.cfg_file}, dry_run={self.dry_run}, do_upgrade={self.do_upgrade})"

    def upgrade(self, revision: str = "head") -> None:
        """Upgrade the database, or simulate with --dry-run.

        Args:
            revision (str, optional): Revision to upgrade to. Defaults to "head".
            dry_run (bool, optional): Simulate upgrade. Defaults to False.

        Raises:
            Exception: If an error occurs during upgrade.

        """
        log.info(
            f"{'Simulating' if self.dry_run else 'Upgrading'} to revision: {revision}"
        )
        try:
            command.upgrade(self.config, revision, sql=self.dry_run)
            log.info(
                f"Database {('would be ' if self.dry_run else '')}upgraded to: {revision}"
            )
        except Exception as exc:
            log.error(f"({type(exc)}) Error during upgrade: {exc}")
            raise exc

    def downgrade(self, revision: str = "-1") -> None:
        """Downgrade the database, or simulate with --dry-run.

        Args:
            revision (str, optional): Revision to downgrade to. Defaults to "-1".

        Raises:
            Exception: If an error occurs during downgrade.

        """
        log.info(
            f"{'Simulating' if self.dry_run else 'Downgrading'} to revision: {revision}"
        )

        try:
            if self.dry_run:
                ## Get the current revision before proceeding
                script = self.config.get_main_option("script_location")

                ## Create ScriptDirectory object
                script_directory = ScriptDirectory.from_config(self.config)
                ## Get current head
                current_head = script_directory.get_current_head()

                if not current_head:
                    raise ValueError(
                        "Cannot determine the current revision for --sql mode."
                    )

                ## Target revision to downgrade to
                downgrade_target = f"{current_head}:{revision}"
            else:
                downgrade_target = revision

            if not self.dry_run:
                ## Downgrade the database
                command.downgrade(self.config, downgrade_target, sql=self.dry_run)

            log.info(
                f"Database {('would be ' if self.dry_run else '')}downgraded to: {downgrade_target}"
            )
        except Exception as exc:
            log.error(f"({type(exc)}) Error during downgrade: {exc}")
            raise exc

    def create_migration(
        self,
        message: str = "autogenerated migration",
    ):
        """Generate a new migration file.

        Args:
            message (str, optional): Message for the migration. Defaults to "autogenerated migration".
            do_upgrade (bool, optional): Upgrade the database after creating the migration. Defaults to False.
            dry_run (bool, optional): Simulate migration creation. Defaults to False.

        Raises:
            Exception: If an error occurs during migration creation.

        """
        if self.dry_run:
            log.info(
                f"[DRY-RUN] Would create migration with message: {message}{', and would upgrade the database' if self.do_upgrade else ''}"
            )
            return

        log.info(f"Creating migration: {message}")
        try:
            command.revision(self.config, message=message, autogenerate=True)
            log.info(f"Migration created: {message}")
        except Exception as exc:
            log.error(f"({type(exc)}) Error creating migration: {exc}")
            raise exc

        if self.do_upgrade:
            log.info(f"Upgrading database after creating migration: {message}")
            if not self.dry_run:
                self.upgrade("head")
