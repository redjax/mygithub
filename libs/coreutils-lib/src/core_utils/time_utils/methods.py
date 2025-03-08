from __future__ import annotations

import typing as t
from datetime import (
    datetime as dt,
)
import time
from typing import Union

from .constants import TIME_FMT_12H, TIME_FMT_24H

from loguru import logger as log


def datetime_as_str(
    ts: dt, format: str = TIME_FMT_24H, safe_str: bool = False
) -> str:
    """Convert a `datetime.datetime` object to a string.

    Params:
        ts (datetime.datetime): A Python `datetime.datetime` object to convert to a `str`
        format (str): The `str` time string format to use
        safe_str (bool): (default: False) When `True`, replace characters to make the path safe for all OSes.

    Returns:
        (str): A formatted `datetime.datetime` `str`

    """
    path_char_replacements = {
        ":": "-",
        "\\": "/",
        "*": "(all)",
        '"': "'",
        "|": "_",
        "?": "-_-",
    }
    _ts: str = ts.strftime(format=format)

    if safe_str:
        for char in path_char_replacements.keys():
            if char in _ts:
                _ts = _ts.replace(char, path_char_replacements[char])

    return _ts


def datetime_as_dt(ts: str, format: str = TIME_FMT_24H) -> dt:
    """Convert a datetime string to a `datetime.datetime` object.

    Params:
        ts (str): A datetime str to convert to a Python `datetime.datetime` object
        format (str): The `str` time string format to use

    Returns:
        (str): A formatted `datetime.datetime` object

    """
    _ts: dt = dt.strptime(ts, format)

    return _ts


def get_ts(
    as_str: bool = False, safe_str: bool = False, format: str = TIME_FMT_24H
) -> Union[dt, str]:
    """Get a timestamp object.

    Params:
        as_str (bool): If `True`, converts `datetime` to a `str`
        format (str): The `str` time string format to use

    Returns:
        (datetime.datetime): a Python `datetime.datetime` object.
        (str): If `as_str` is `True`, converts datetime to a string & returns.

    """
    now: dt = dt.now()

    if as_str:
        _now: str = datetime_as_str(ts=now, format=format, safe_str=safe_str)

    return _now


def wait(s: int = 1, msg: str | None = "Waiting {} seconds...") -> None:
    """Sleep for a number of seconds, with optional custom message.

    Params:
        s (int): Amount of time (in seconds) to sleep/pause.
        msg (str): [default: 'Wating {} seconds...'] A custom message to print. Use {} in the
            message to print the value of s.

                Example: 'I will now wait for {} second(s)' => 'I will now wait for 15 seconds...'
    """
    assert s, ValueError("Missing amount of time to sleep")
    assert isinstance(s, int) and s > 0, ValueError(
        f"Value of s must be a positive, non-zero integer. Input value ({type(s)}): {s} is invalid."
    )

    ## If msg != None, validate & print before pausing
    if msg:
        ## Validate & print pause message
        assert isinstance(msg, str), TypeError(
            f"msg must be a string or None. Got type: ({type(msg)})"
        )

        try:
            log.info(msg.format(s))
        except Exception as exc:
            ## Error compiling message text. Print an error, then wait
            wait_msg_err = Exception(
                f"Unhandled exception composing wait message. Details: {exc}.\nWaiting [{s}] seconds..."
            )
            log.error(wait_msg_err)

    ## Pause
    time.sleep(s)
