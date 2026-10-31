# Deletes the data stored under the key's position in memory
# And adds delete order to .txt
def delete(key: str, dataset: dict[str, str], path: str) -> str:
    if key in dataset:
        del dataset[key]

        with open(path, 'a') as file:
            file.write("?" + str(key) + "\n")
        return "deleted data with key:" + key
    else:
        raise KeyError