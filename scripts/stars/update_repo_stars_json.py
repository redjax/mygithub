from loguru import logger as log

import setup
from project_cli.subcommands.github.gh_stars import get_user_stars
from cli_spinners import CustomSpinner

if __name__ == "__main__":
    setup.setup_loguru_logging(log_level="WARNING", colorize=True)

    try:
        with CustomSpinner("Updating my_stars.json"):
            get_user_stars(
                save_db=False, save_json=True, json_file="my_stars.json", use_cache=True
            )
    except Exception as e:
        print(f"[ERROR] Error updating my_stars.json. Details: {e}")
        exit(1)
