# Change here if you want to use a different file for the database
FILE = 'data2.txt'
dataset = [""] * 100
# Creates the data file if it doesn't exist, leaves existing data alone
def init():
    open (FILE, 'a').close()
    return "Data file ready"

# Wipes the dataset clean
# Reads line by line, and executes the order in each line
# Either key:data or delete data in key (?xxx)
def getdata():

    for i in range(100):
        dataset[i] = ""

    with open (FILE, 'r') as file:
        for line in file:
            line = line.rstrip("\n")
            if line[0] == '?':
                line = line.lstrip("?")
                key = line
                position = convert(key)
                dataset[position] = ""
            else:
                key, data = line.split(":")
                position = convert(key)
                dataset[position] = data

# Not needed here
# Database updates in real time
# Writes the dictionary (in format: position: data) in the file (overwrite)
#def writelines():
#    with open (FILE, 'w') as file:
#        for position in dataset:
#            file.write(str(position) + ":" + dataset[position] + "\n")
#    return "Data file updated"

# Converts a key into a position by concatenating the ASCII values of each character in the key
# Lets limit it to 100 total possible entries
def convert(key):
    position = ""
    for c in key:
        position = position + str(ord(c))
    position = int(position)
    position = position % 100
    return position

# Saves data under the key's position (overwrites if something was already there)
# Both creates an entry in .txt and in memory
def set(key, data):
    position = convert(key)
    if dataset[position] == data:
        return "Already exists"
    with open(FILE, 'a') as file:
        file.write(key + ":" + data + "\n")
    dataset[position] = data
    return "saved " + "\"" + data + "\"" + " in position:" + str(position)

# Gets the data stored under the key's position
# Directly from the dataset
def get(key):
    position = convert(key)
    return dataset[position]

# Deletes the data stored under the key's position in memory
# And adds delete order to .txt
def delete(key):
    position = convert(key)
    if dataset[position] == "":
        return "Doesnt exist"

    with open(FILE, 'a') as file:
        file.write("?" + str(key) + "\n")
    return "deleted data in position:" + str(position)

# Testing
init()
getdata()
print(set("key1", "data1"))
print(set("key2", "data2"))
#print(set("key3", "data3"))
print(delete("key3"))
print(dataset)
