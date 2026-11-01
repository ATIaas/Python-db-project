from .log_line import delete_line

# Deletes the data stored under the key's position in memory
# And adds delete order to .txt
def delete(key: str, dataset: dict[str, str], path: str) -> str:
    if key in dataset:
        del dataset[key]

        with open(path, 'a') as file:
            file.write(delete_line(key))
        return "deleted data with key:" + key
    else:
        raise KeyError