# Deletes the data stored under the key's position in memory
# And adds delete order to .txt
def delete(key, dataset, FILE):
    if key in dataset:
        del dataset[key]

        with open(FILE, 'a') as file:
            file.write("?" + str(key) + "\n")
        return "deleted data with key:" + key
    else:
        raise KeyError