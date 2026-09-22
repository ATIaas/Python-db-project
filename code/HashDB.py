#This program uses the direct text file for operations
#Instead of a giant array
#Makes it easier to see
def init():
    lines = 1000000
    with open ('data.txt', 'w') as file:
        for x in range(lines):
            file.write("\n")
    return "Initiated text file with " + str(lines) + " lines"

#These two could use another parameter for file
def getlines():
    with open ('data.txt', 'r') as file:
        dataset = file.readlines()
    return dataset

def writelines(dataset):
    with open ('data.txt', 'w') as file:
        file.writelines(dataset)

def convert(key):
    position = ""
    for c in key:
        position = position + str(ord(c))
    position = int(position)
    return position

#Position 0 is not really used
def set(key, data):
    dataset = getlines()
    position = convert(key)
    dataset[position] = data
    writelines(dataset)
    return "saved " + "\"" + data + "\"" + " in position:" + str(position)

def get(key):
    position = convert(key)
    dataset = getlines()

    return dataset[position]

def delete(key):
    position = convert(key)
    dataset = getlines()
    dataset[position] = "\n"
    writelines(dataset)
    return "deleted data: " + key + " from position: " + str(position)