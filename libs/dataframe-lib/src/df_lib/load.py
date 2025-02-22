from loguru import logger as log

import settings, db_lib
import sqlalchemy as sa
import sqlalchemy.orm as so
import sqlalchemy.exc as sa_exc
import pandas as pd

__all__ = ["load_df_from_sql"]


def load_df_from_sql(table_name: str, db_engine: sa.Engine):
    if not db_engine:
        log.error("Missing a SQLAlchemy Engine object")
        return
    if not table_name:
        log.error("Missing a database table name")
        return

    log.debug(f"Detected database dialect: {db_engine.dialect.name}")
    log.info(f"Reading table into DataFrame: {table_name}")
    try:
        df: pd.DataFrame = pd.read_sql_table(table_name=table_name, con=db_engine)

        return df
    except Exception as exc:
        msg = f"({type(exc)}) error"
        log.error(msg)

        raise exc
