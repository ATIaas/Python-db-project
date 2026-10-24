# Saves data under the key's position (overwrites if something was already there)
# Both creates an entry in .txt and in memory
# Raises ValueError if key or data would corrupt the log
def set(key, data, dataset, FILE):
    if key == "":
        raise ValueError("key cannot be empty")
    if ":" in key:
        raise ValueError("key cannot contain \":\"")
    if key.startswith("?"):
        raise ValueError("key cannot start with \"?\"")
    if "\n" in key or "\n" in data:
        raise ValueError("key and data cannot contain line breaks")

    if key in dataset:
        if dataset[key] == data:
            return "Already exists"

    #Write to log and update dataset
    with open(FILE, 'a') as file:
        file.write(key + ":" + data + "\n")
    dataset[key] = data
    return "saved " + "\"" + data + "\"" + " in key:" + key