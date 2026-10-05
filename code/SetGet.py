import DicConvert as con
# Saves data under the key's position (overwrites if something was already there)
# Both creates an entry in .txt and in memory
def set(key, data, dataset, FILE):
    position = con.convert(key)
    if dataset[position] == data:
        return "Already exists"
    with open(FILE, 'a') as file:
        file.write(key + ":" + data + "\n")
    dataset[position] = data
    return "saved " + "\"" + data + "\"" + " in position:" + str(position)


# Gets the data stored under the key's position
# Directly from the dataset
def get(key, dataset):
    position = con.convert(key)
    return dataset[position]