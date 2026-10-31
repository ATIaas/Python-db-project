# Deletes the data stored under the key's position in memory
# And adds delete order to .txt
def delete(key: str, dataset: dict[str, str], FILE: str) -> str:
    if key in dataset:
        del dataset[key]

        with open(FILE, 'a') as file:
            file.write("?" + str(key) + "\n")
        return "deleted data with key:" + key
    else:
        raise KeyError