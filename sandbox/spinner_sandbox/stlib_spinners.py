from __future__ import annotations

import time

from core_utils import spinner_utils
from loguru import logger as log
import setup

if __name__ == "__main__":
    setup.setup_loguru_logging(log_level="DEBUG", colorize=True)

    log.info("Test stdlib spinner")

    with spinner_utils.SimpleSpinner("Sleeping for 3 seconds..."):
        time.sleep(3)

        raise ValueError("Test exception")
