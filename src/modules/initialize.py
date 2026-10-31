import os

from .parse import parse

def start_dataset(path: str) -> dict[str, str]:
    """Reads the log and returns the latest value of each live key."""
    if not os.path.exists(path):
        open(path, 'w').close()
    db: dict[str, str] = {}
    with open(path, "r") as f:
        lines: list[str] = f.readlines()
    for line in lines:
        parse(line, db)
    return db