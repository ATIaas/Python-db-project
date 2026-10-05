import DicConvert as con

# Wipes the dataset clean
# Reads line by line, and executes the order in each line
# Either key:data or delete data in key (?xxx)
def getdata(FILE):
    dataset = [""] * 100

    with open(FILE, 'r') as file:
        for line in file:
            line = line.rstrip("\n")
            if line[0] == '?':
                line = line.lstrip("?")
                key = line
                position = con.convert(key)
                dataset[position] = ""
            else:
                key, data = line.split(":")
                position = con.convert(key)
                dataset[position] = data

    return dataset