from loguru import logger as log
import settings, setup, db_lib
from depends import db_depends

from domain import github as github_domain
from datalab import df_ops

import sqlalchemy as sa

import pandas as pd


def main(db_engine: sa.Engine):
    log.debug(f"DB engine dialect: {db_engine.dialect.name}")

    log.info("Building dataframe from database table: 'gh_starred_repo'")
    try:
        starred_df: pd.DataFrame = df_ops.load.load_df_from_sql(
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
        df_ops.save.save_df_to_pq(
            df=starred_df, output_file=".data/output/pq/gh_starred_repo.parquet"
        )
        log.info(
            "Saved starred repos to parquet file: ./data/output/pq/gh_starred_repo.parquet"
        )
    except Exception as exc:
        msg = f"({type(exc)}) Error saving github starred repositories: {exc}"
        log.error(msg)

        raise


if __name__ == "__main__":
    setup.setup_loguru_logging(
        log_level=settings.LOGGING_SETTINGS.get("LOG_LEVEL", default="INFO"),
        colorize=True,
    )
    setup.setup_database()

    db_engine = db_depends.get_db_engine()

    main(db_engine=db_engine)
