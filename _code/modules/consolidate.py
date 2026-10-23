def load_latest(path: str) -> dict:
    """Reads the log and returns the latest value of each live key."""
    db = {}
    with open(path, "r") as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("?"):
                db.pop(line[1:], None)      # delete order
            elif ":" in line:
                key, data = line.split(":", 1)
                db[key] = data              # newer value overwrites older
    return db


def write_all(path: str, db: dict) -> None:
    """Overwrites the file with the given key:data pairs."""
    with open(path, "w") as f:
        for key, data in db.items():
            f.write(f"{key}:{data}\n")


def consolidate(path: str) -> None:
    write_all(path, load_latest(path))