def set_line(key: str, data: str) -> str:
    """Returns the log line that saves data under key."""
    return key + ":" + data + "\n"

def delete_line(key: str) -> str:
    """Returns the log line that deletes key."""
    return "?" + key + "\n"
