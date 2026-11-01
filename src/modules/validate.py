def validate_key(key: str) -> None:
    """Raises ValueError if the key would corrupt the log."""
    if key == "":
        raise ValueError("key cannot be empty")
    if ":" in key:
        raise ValueError("key cannot contain \":\"")
    if key.startswith("?"):
        raise ValueError("key cannot start with \"?\"")
    if "\n" in key:
        raise ValueError("key cannot contain line breaks")

def validate_data(data: str) -> None:
    """Raises ValueError if the data would corrupt the log."""
    if "\n" in data:
        raise ValueError("data cannot contain line breaks")
