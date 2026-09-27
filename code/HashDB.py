# Change here if you want to use a different file for the database
FILE = 'data.txt'

# Creates the data file if it doesn't exist, leaves existing data alone
def init():
    open (FILE, 'a').close()
    return "Data file ready"

# Reads the file and gives back a dictionary (position: data) skipping empty lines
def getlines():
    dataset = {}
    with open (FILE, 'r') as file:
        for line in file:
            line = line.rstrip("\n")
            if line != "":
                position, data = line.split(":")
                dataset[int(position)] = data
    return dataset

# Writes the dictionary (in format: position: data) in the file (overwrite)
def writelines(dataset):
    with open (FILE, 'w') as file:
        for position in dataset:
            file.write(str(position) + ":" + dataset[position] + "\n")
    return "Data file updated"

# Converts a key into a position by concatenating the ASCII values of each character in the key
def convert(key):
    position = ""
    for c in key:
        position = position + str(ord(c))
    position = int(position)
    return position

# Saves data under the key's position (overwrites if something was already there)
def set(key, data):
    dataset = getlines()
    position = convert(key)
    dataset[position] = data
    writelines(dataset)
    return "saved " + "\"" + data + "\"" + " in position:" + str(position)

# Gets the data stored under the key's position
def get(key):
    position = convert(key)
    dataset = getlines()
    return dataset[position]

# Deletes the data stored under the key's position and overwrite the file (db)
def delete(key):
    position = convert(key)
    dataset = getlines()
    dataset.pop(position)
    writelines(dataset)
    return "deleted data in position:" + str(position)