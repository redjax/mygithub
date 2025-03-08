from __future__ import annotations

import logging
from pathlib import Path
import typing as t

import pandas as pd

log = logging.getLogger(__name__)

__all__ = [
    "save_pq",
    "save_csv",
    "save_json",
]


def save_pq(
    df: pd.DataFrame,
    pq_file: t.Union[str, Path],
    dedupe: bool = False,
    pq_engine: str = "pyarrow",
) -> bool:
    """Save DataFrame to a .parquet file.

    Params:
        df (pandas.DataFrame): A Pandas `DataFrame` to save
        pq_file (str|Path): The path to a `.parquet` file where the `DataFrame` should be saved
        dedupe (bool): If `True`, deduplicate the `DataFrame` before saving

    Returns:
        (bool): `True` if `DataFrame` is saved to `pq_file` successfully
        (bool): `False` if `DataFrame` is not saved to `pq_file` successfully

    Raises:
        Exception: If file cannot be saved, an `Exception` is raised

    """
    if df is None or df.empty:
        msg = ValueError("DataFrame is None or empty")
        log.warning(msg)

        return False

    if pq_file is None:
        raise ValueError("Missing output path")
    if isinstance(pq_file, str):
        _pq_filepath: Path = Path(pq_file)

    if _pq_filepath.suffix != ".parquet":
        new_str = str(f"{_pq_filepath}.parquet")
        _pq_file: Path = Path(new_str)

    if not _pq_file.parent.exists():
        try:
            _pq_file.parent.mkdir(exist_ok=True, parents=True)
        except Exception as exc:
            mkdir_err_msg: Exception = Exception(
                f"Unhandled exception creating directory: {_pq_file.parent}. Details: {exc}"
            )
            log.error(mkdir_err_msg)

            return False

    try:
        if dedupe:
            df = df.drop_duplicates()

        output = df.to_parquet(path=pq_file, engine=pq_engine) # type: ignore

        return True

    except Exception as exc:
        save_df_err_msg = Exception(
            f"Unhandled exception saving DataFrame to Parquet file: {_pq_file}. Details: {exc}"
        )
        log.error(save_df_err_msg)
        raise exc


def save_csv(
    df: pd.DataFrame,
    csv_file: t.Union[str, Path],
    columns: list[str],
    dedupe: bool = False,
) -> bool:
    """Save DataFrame to a .csv file.

    Params:
        df (pandas.DataFrame): A Pandas `DataFrame` to save
        csv_file (str|Path): The path to a `.csv` file where the `DataFrame` should be saved
        columns (list[str]): A list of string values representing column names for the `.csv` file
        dedupe (bool): If `True`, deduplicate the `DataFrame` before saving

    Returns:
        (bool): `True` if `DataFrame` is saved to `csv_file` successfully
        (bool): `False` if `DataFrame` is not saved to `csv_file` successfully

    Raises:
        Exception: If file cannot be saved, an `Exception` is raised

    """
    if df is None or df.empty:
        msg = ValueError("DataFrame is None or empty")

        return False

    if csv_file is None:
        raise ValueError("Missing output path")
    if isinstance(csv_file, str):
        _csv_file: Path = Path(csv_file)

    if _csv_file.suffix != ".csv":
        new_str = str(f"{_csv_file}.csv")
        csv_filepath: Path = Path(new_str)

    if not csv_filepath.parent.exists():
        try:
            csv_filepath.parent.mkdir(exist_ok=True, parents=True)
        except Exception as exc:
            csv_mkdir_err_msg = Exception(
                f"Unhandled exception creating directory: {_csv_file.parent}. Details: {exc}"
            )
            log.error(csv_mkdir_err_msg)

            return False

    if columns is None:
        columns = df.columns

    try:
        if dedupe:
            df = df.drop_duplicates()

        if columns is not None:
            output = df.to_csv(csv_file, columns=columns)
        else:
            output = df.to_csv(csv_file)

        return True

    except Exception as exc:
        save_df_err_msg = Exception(
            f"Unhandled exception saving DataFrame to Parquet file: {csv_file}. Details: {exc}"
        )
        log.error(save_df_err_msg)
        raise exc


def save_json(
    df: pd.DataFrame,
    json_file: t.Union[str, Path],
    indent: int | None = None,
) -> bool:
    """Save DataFrame to a .json file.

    Params:
        df (pandas.DataFrame): A Pandas `DataFrame` to save
        json_file (str|Path): The path to a `.json` file where the `DataFrame` should be saved

    Returns:
        (bool): `True` if `DataFrame` is saved to `json_file` successfully
        (bool): `False` if `DataFrame` is not saved to `json_file` successfully

    Raises:
        Exception: If file cannot be saved, an `Exception` is raised

    """
    if df is None or df.empty:
        msg = ValueError("DataFrame is None or empty")
        log.warning(msg)

        return False

    if json_file is None:
        raise ValueError("Missing output path")
    if isinstance(json_file, str):
        json_filepath: Path = Path(json_file)

    if json_filepath.suffix != ".json":
        new_str = str(f"{json_file}.json")
        _json_filepath: Path = Path(new_str)

    if not _json_filepath.parent.exists():
        try:
            _json_filepath.parent.mkdir(exist_ok=True, parents=True)
        except Exception as exc:
            json_dir_err_msg = Exception(
                f"Unhandled exception creating directory: {_json_filepath.parent}. Details: {exc}"
            )
            log.error(json_dir_err_msg)

            return False

    try:
        df.to_json(json_file, orient="records", indent=indent)
        return True

    except Exception as exc:
        save_json_err_msg = Exception(
            f"Unhandled exception saving DataFrame to JSON file: {json_file}. Details: {exc}"
        )
        log.error(save_json_err_msg)
        raise exc
