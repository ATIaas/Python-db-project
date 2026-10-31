import os

def start_dataset(FILE: str) -> dict[str, str]:
    """Reads the log and returns the latest value of each live key."""
    if not os.path.exists(FILE):
        open(FILE, 'w').close()
    db: dict[str, str] = {}
    with open(FILE, "r") as f:
        lines = f.readlines()
    for line in lines:
        line = line.rstrip("\n")
        if line.startswith("?"):
            db.pop(line[1:], None)  # delete order
        elif ":" in line:
            key, data = line.split(":", 1)
            db[key] = data  # newer value overwrites older
    return db
