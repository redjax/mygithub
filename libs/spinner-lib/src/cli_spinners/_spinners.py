import typing as t
from halo import Halo # type: ignore

__all__ = ["CustomSpinner"]


class CustomSpinner:
    def __init__(
        self,
        text: str = "Loading",
        spinner: str = "dots",
        color: str = "cyan",
        text_color: str | None = None,
        animation: t.Any | None = "marquee",
        placement: str = "left",
        interval: int = -1,
    ):
        self.spinner = Halo(
            text=text,
            spinner=spinner,
            text_color=text_color,
            color=color,
            animation=animation,
            placement=placement,
            interval=interval,
        )

    def __enter__(self):
        self.spinner.start()
        return self.spinner

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.spinner.succeed("Operation completed successfully")
        else:
            self.spinner.fail("Operation failed")

        self.spinner.stop()
