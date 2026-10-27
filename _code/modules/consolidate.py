import os
import tempfile


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
    """Replaces the file atomically with the given key:data pairs."""
    dir_ = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(dir=dir_, prefix=".consolidate-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            for key, data in db.items():
                f.write(f"{key}:{data}\n")
            f.flush()
            os.fsync(f.fileno())            # make sure the bytes reached the disk

        try:                                # keep the original file's permissions
            os.chmod(tmp, os.stat(path).st_mode & 0o7777)
        except FileNotFoundError:
            pass

        os.replace(tmp, path)               # atomic swap
    except BaseException:
        try:
            os.unlink(tmp)                  # don't leave a stray temp file behind
        except FileNotFoundError:
            pass
        raise


def consolidate(path: str) -> None:
    write_all(path, load_latest(path))