import os
import tempfile

from .log_line import set_line

#I think the tmp file size exception needs to be a separate issue

def consolidate(path: str, db: dict[str, str]) -> None:
    """Replaces the file atomically with the given key:data pairs."""
    dir_: str = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(dir=dir_, prefix=".consolidate-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            for key, data in db.items():
                f.write(set_line(key, data))
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