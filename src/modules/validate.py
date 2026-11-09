from .exceptions import DBValueError, DBKeyError

def validate_key(key: str) -> None:
    """Raises ValueError if the key would corrupt the log."""
    if key == "":
        raise DBKeyError("key cannot be empty")
    if ":" in key:
        raise DBKeyError("key cannot contain \":\"")
    if key.startswith("?"):
        raise DBKeyError("key cannot start with \"?\"")
    if "\n" in key:
        raise DBKeyError("key cannot contain line breaks")

def validate_data(data: str) -> None:
    """Raises ValueError if the data would corrupt the log."""
    if "\n" in data:
        raise DBValueError("data cannot contain line breaks")
