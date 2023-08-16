from pathlib import Path


def get_webapp_root() -> Path:
    # enables running the "taqo" cmd (aka starting the webpage) from wherever
    return Path(__file__).parent.parent.parent
