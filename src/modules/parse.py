def parse(line: str, db: dict[str, str]) -> None:
    """Applies one line of the log to db: key:data saves the data, ?key deletes the key."""
    line = line.rstrip("\n")
    if line.startswith("?"):
        key = line[1:]
        if key in db:
            del db[key]
    elif ":" in line:
        key, data = line.split(":", 1)
        db[key] = data