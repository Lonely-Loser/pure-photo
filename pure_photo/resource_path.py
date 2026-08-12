from pathlib import Path
import sys


def resource_path(*paths) -> str:
    """
    Return the absolute path to a bundled resource.

    Works both:
        - from source
        - from a PyInstaller executable
    """
    if getattr(sys, "frozen", False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent

    return str(base_path.joinpath(*paths))
