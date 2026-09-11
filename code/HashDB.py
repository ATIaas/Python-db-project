
#Idk why i am doing a string return
#Sue me
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
        file = file.writelines(dataset)

def convert(data):
    position = ""
    for c in data:
        position = position + str(ord(c))
    position = int(position)
    return position

#Position 0 is not really used
def set(data):
    dataset = getlines()
    position = convert(data)
    dataset[position] = data
    writelines(dataset)
    return "saved " + "\"" + data + "\"" + " in position:" + str(position)

def get(data):
    exists = False
    position = convert(data)
    dataset = getlines()

    if dataset[position] == data + "\n":
        exists = True

    return position, exists

print(init())
print(set("ch"))
print(get("c"))
print(get("ch"))