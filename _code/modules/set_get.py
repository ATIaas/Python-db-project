# Saves data under the key's position (overwrites if something was already there)
# Both creates an entry in .txt and in memory
def set(key, data, dataset, FILE):
    if key in dataset:
        return "Already exists"
    with open(FILE, 'a') as file:
        file.write(key + ":" + data + "\n")
    dataset[key] = data
    return "saved " + "\"" + data + "\"" + " in key:" + key


# Gets the data stored under the key's position
# Directly from the dataset
def get(key, dataset):
    return dataset[key]