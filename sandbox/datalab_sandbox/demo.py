from __future__ import annotations

from core_utils import df_utils
import db_lib
from depends import db_depends
from domain import github as github_domain
from loguru import logger as log
import pandas as pd
import settings
import setup
import sqlalchemy as sa


def main(db_engine: sa.Engine):
    log.debug(f"DB engine dialect: {db_engine.dialect.name}")

    log.info("Building dataframe from database table: 'gh_starred_repo'")
    try:
        starred_df: pd.DataFrame = df_utils.io.load_sql(
            table_name="gh_starred_repo", db_engine=db_engine
        )
    except Exception as exc:
        msg = f"({type(exc)}) error"
        log.error(msg)

        raise exc

    if not isinstance(starred_df, pd.DataFrame) or starred_df.empty:
        log.error("DataFrame is empty.")
        return

    log.info(f"First 10 results:\n{starred_df.head(10)}")

    log.info(f"Saving dataframe to .data/output/pq/gh_starred_repo.parquet")
    try:
        df_utils.io.save_pq(
            df=starred_df, pq_file=".data/output/pq/gh_starred_repo.parquet"
        )
    except Exception as exc:
        msg = f"({type(exc)}) Error saving github starred repositories: {exc}"
        log.error(msg)

        raise

    log.info("Attempting to load saved Parquet data")
    try:
        saved_starred_df = df_utils.io.load_pq(
            pq_file=".data/output/pq/gh_starred_repo.parquet"
        )
    except Exception as exc:
        msg = f"({type(exc)}) Error loading saved Parquet data: {exc}"
        log.error(msg)

        raise

    if not isinstance(saved_starred_df, pd.DataFrame) or saved_starred_df.empty:
        log.error("Saved DataFrame is empty.")
        return

    log.info(f"First 10 results from saved Parquet data:\n{saved_starred_df.head(10)}")


if __name__ == "__main__":
    setup.setup_loguru_logging(
        log_level=settings.LOGGING_SETTINGS.get("LOG_LEVEL", default="INFO"),
        colorize=True,
    )
    setup.setup_database()

    db_engine = db_depends.get_db_engine()

    main(db_engine=db_engine)
