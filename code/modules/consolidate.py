# Consolidates the database by removing duplicates and delete orders
# Rewrites the file with only the latest valid entries
def consolidate(FILE: str) -> None:
    """
    Removes duplicates and delete orders from the file
    Keeps only the latest valid version of each key
    """
    seen_keys = {}

    # Reads the file and keeps the most recent record of each key
    with open(FILE, 'r') as file:
        for line in file:
            line = line.rstrip("\n")
            if not line:
                continue

            if line[0] == '?':
                # It is a delete order
                key = line.lstrip("?")
                seen_keys[key] = None  # None means it was deleted
            else:
                # It is a key:data pair
                if ':' in line:
                    key, data = line.split(":", 1)
                    seen_keys[key] = data

    # Rewrites the file with only the valid (non-deleted) entries
    with open(FILE, 'w') as file:
        for key, data in seen_keys.items():
            if data is not None:  # Only writes if it was not deleted
                file.write(key + ":" + data + "\n")