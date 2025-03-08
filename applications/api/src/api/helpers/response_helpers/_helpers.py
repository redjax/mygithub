from __future__ import annotations

from pathlib import Path
import typing as t

# from helpers import validators
from loguru import logger as log

__all__ = ["stream_file_contents"]


def stream_file_contents(f_path: t.Union[str, Path] | None = None, mode: str = "rb"):
    if f_path is None:
        log.warning(ValueError("Missing a file path"))
        return None

    _path: Path = (
        Path(str(f_path)).expanduser() if "~" in str(f_path) else Path(str(f_path))
    )

    if not _path.exists():
        log.error(f"Could not find  file: '{_path}'.")
        raise FileNotFoundError(f"Could not find  file: '{_path}'.")

    with open(_path, mode=mode) as f_out:
        yield from f_out
