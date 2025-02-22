from loguru import logger as log

import typing as t
from pathlib import Path

import settings, db_lib
import sqlalchemy as sa
import sqlalchemy.orm as so
import sqlalchemy.exc as sa_exc
import pandas as pd

__all__ = ["save_df_to_pq"]


def save_df_to_pq(
    df: pd.DataFrame, output_file: t.Union[str, Path], engine: str = "pyarrow"
):
    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            f"Invalid type for DataFrame: ({type(df)}). Must be a Pandas DataFrame"
        )
    if df.empty:
        raise ValueError("Cannot save empty DataFrame")
    if not output_file:
        raise ValueError("Missing Parquet file output path")

    output_file: Path = (
        Path(str(output_file)).expanduser()
        if "~" in str(output_file)
        else Path(str(output_file))
    )
    if not output_file.parent.exists():
        log.warning(
            f"Parent directory for '{output_file}' does not exist. Creating path)"
        )
        try:
            output_file.parent.mkdir(parents=True, exist_ok=True)
            log.info(f"Created path: '{output_file.parent}'")
        except Exception as exc:
            msg = f"({type(exc)}) Error creating output path: {exc}"
            log.error(msg)

            raise exc

    log.info(f"Saving DataFrame to Parquet file: '{output_file}'")
    try:
        df.to_parquet(str(output_file), engine=engine)
        log.info(f"Saved DataFrame to Parquet file: '{output_file}'")
    except Exception as exc:
        msg = f"({type(exc)}) Error saving DataFrame to Parquet file: {exc}"
        log.error(msg)

        raise exc
