# Change here if you want to use a different file for the database
FILE = 'data.txt'

# In-memory copy of the database (key: data)
# The file is only a log of operations, this is the real current state
dataset = {}

# Creates the data file if it doesn't exist, leaves existing data alone
# Then loads the file into memory
def init():
    open (FILE, 'a').close()
    load()
    return "Data file ready"

# Wipes the dataset clean
# Reads line by line, and executes the order in each line
# Either key:data (set) or ?key (delete)
# Keys can't contain ':' so a line without ':' is always a delete
def load():
    dataset.clear()
    with open (FILE, 'r') as file:
        for line in file:
            line = line.rstrip("\n")
            if line != "":
                if line[0] == '?' and ":" not in line:
                    key = line[1:]
                    dataset.pop(key, None)
                else:
                    key, data = line.split(":", 1)
                    dataset[key] = data

# Saves data under the key (overwrites if something was already there)
# Adds the order to the file and updates memory
def set(key, data):
    if ":" in key or key == "":
        return "Invalid key"
    if key in dataset and dataset[key] == data:
        return "Already exists"
    with open (FILE, 'a') as file:
        file.write(key + ":" + data + "\n")
    dataset[key] = data
    return "saved " + "\"" + data + "\"" + " in key:" + key

# Gets the data stored under the key directly from memory
# Returns None if the key doesn't exist
def get(key):
    return dataset.get(key)

# Deletes the data stored under the key in memory
# And adds delete order to the file
def delete(key):
    if key not in dataset:
        return "Doesnt exist"
    with open (FILE, 'a') as file:
        file.write("?" + key + "\n")
    dataset.pop(key)
    return "deleted data in key:" + key

# Testing (only runs when executing this file directly, not when importing it)
if __name__ == '__main__':
    print(init())
    print(set("key1", "data1"))
    print(set("abc1", "data2"))
    print(set("key3", "data:with:colons"))
    print(delete("key3"))
    print(delete("key3"))
    print(get("key1"), get("abc1"), get("key3"))
    print(dataset)
