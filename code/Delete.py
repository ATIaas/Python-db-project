import DicConvert as con
# Deletes the data stored under the key's position in memory
# And adds delete order to .txt
def delete(key, dataset, FILE):
    position = con.convert(key)
    if dataset[position] == "":
        return "Doesnt exist"

    dataset[position] = ""

    with open(FILE, 'a') as file:
        file.write("?" + str(key) + "\n")
    return "deleted data in position:" + str(position)