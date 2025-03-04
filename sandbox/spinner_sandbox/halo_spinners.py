import time
from cli_spinners import CustomSpinner

if __name__ == "__main__":
    with CustomSpinner(text="Sleeping for 3 seconds...", spinner="dots", color="green"):
        time.sleep(3)