import os

def start_dataset(FILE: str) -> dict[str, str]:
    # Creates the data file if it doesn't exist, leaves existing data alone
    if not os.path.exists(FILE):
        open(FILE, 'w').close()
    # Wipes the dataset clean
    # Reads line by line, and executes the order in each line
    # Either key:data or delete data in key (?xxx)
    """Reads the log and returns the latest value of each live key."""
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
