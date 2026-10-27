# this function is slightly modified as it recreates the db dict when doing so
import os
import tempfile




def consolidate(S) :
    """Replaces the file atomically with the given key:data pairs."""

    S._initialize_the_DB()


    dir_ = os.path.dirname(os.path.abspath(S._file_path))
    fd, tmp = tempfile.mkstemp(dir=dir_, prefix=".consolidate-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding=S._encoding) as file:
            for key, value in S._dictDB.items():
                file.write(str(key) + ":" + str(value) + "\r\n")
            file.flush()
            os.fsync(file.fileno())  # make sure the bytes reached the disk

        try:  # keep the original file's permissions
            os.chmod(tmp, os.stat(S._file_path).st_mode & 0o7777)
        except FileNotFoundError:
            pass

        os.replace(tmp, S._file_path)  # atomic swap
    except BaseException:
        try:
            os.unlink(tmp)  # don't leave a stray temp file behind
        except FileNotFoundError:
            pass
        raise