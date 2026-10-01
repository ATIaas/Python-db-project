import io



# Change here if you want to use a different file for the database
FILE = 'data3'
dataset = [""] * 100
# Creates the data file if it doesn't exist, leaves existing data alone
def init():
    open (FILE, 'a').close()
    return "Data file ready"


class binary_utf32_file_reader:

    __current_uchar_chunk = b""
    __EoF = False

    def __byte_array_fill__(self):
        chunk = self.file.read(4000) #1000 chars
        if len(chunk) != 4000: self.__EoF = True ;
        self.__current_uchar_chunk = chunk


    def __init__(self, file_name: str):
        self.file_name = file_name
        self.file = open(file_name, 'rb')


    def getline(self)->bytes:
        ret: bytes = b""

        while not (self.__EoF and self.__current_uchar_chunk == b""):
            #pos = self.__current_uchar_chunk.find("\r\n".encode("utf-32")[4:])
            pos = self.__current_uchar_chunk.find(b"\r\x00\x00\x00\n\x00\x00\x00") # is the same as top one but faster as it is hard coded


            if pos != -1:
                ret += self.__current_uchar_chunk[: pos]
                self.__current_uchar_chunk = self.__current_uchar_chunk[pos + 8:]
                return ret


            ret += self.__current_uchar_chunk
            self.__current_uchar_chunk = b""
            self.__byte_array_fill__()

        return ret


    def read_file(self, amount:int = -1)->bytes:
        if (amount == -1):
            return self.file.read()
        return self.file.read(amount)


    def __del__(self):
        self.file.close()


# Wipes the dataset clean
# Reads line by line, and executes the order in each line
# Either key:data or delete data in key (?xxx)
def getdata():

    for i in range(100):
        dataset[i] = ""

    file = binary_utf32_file_reader(FILE)
    line = file.getline()


    while(line != ""):

        line = line.decode("utf-32")
        print(line)
        line = line.rstrip("\n")
        if (line == ""): # basically  b"\xff\xfe\x00\x00" or the utf beggining 2 chars U-(allways apperas in a utf file)
            continue

        if line[0] == '?':
            line = line.lstrip("?")
            key = line
            position = convert(key)
            dataset[position] = ""
        else:
            key, data = line.split(":")
            position = convert(key)
            dataset[position] = data

        line = file.getline()


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
    pos = int(position)
    position = pos % 100
    return position

# Saves data under the key's position (overwrites if something was already there)
# Both creates an entry in .txt and in memory
def set(key, data):
    position = convert(key)
    if dataset[position] == data:
        return "Already exists"
    with open(FILE, 'ab') as file:
        file.write( (str(key + ":" + data + "\r\n")).encode("utf-32"))
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
    if dataset[position] == b"":
        return "Doesnt exist"

    with open(FILE, 'ab') as file:
        file.write((str("?" + str(key) + "\r\n")).encode("utf-32"))
    return "deleted data in position:" + str(position)

# Consolidates the database by removing duplicates and delete orders
# Rewrites the file with only the latest valid entries
#
#ATIaas:: not yet utf-32 compliant
#
def consolidate():
    """
    Elimina duplicados y ordenes de eliminacion del archivo
    Mantiene solo la ultima version valida de cada clave
    """
    seen_keys = {}
    
    # Lee el archivo y mantiene el registro más reciente de cada clave
    with open(FILE, 'rb') as file:
        for line in file:
            line = line.decode("utf-32")
            line = line.rstrip("\n")
            if not line:
                continue
            
            if line[0] == '?':
                # Es una orden de eliminacion
                key = line.lstrip("?")
                seen_keys[key] = None  # None indica que fue eliminado
            else:
                # Es un par key:data
                if ':' in line:
                    key, data = line.split(":", 1)
                    seen_keys[key] = data
    
    # Reescribe el archivo con solo las entradas validas (no eliminadas)
    with open(FILE, 'wb') as file:
        for key, data in seen_keys.items():
            if data is not None:  # Solo escribe si no fue eliminado
                file.write( (str(key + ":" + data + "\r\n")).encode("utf-32"))
    
    # Recarga los datos en memoria
    getdata()
    return "Database consolidated: " + str(len([v for v in seen_keys.values() if v is not None])) + " valid entries"
    
# Testing
init()
getdata()
print(set("key1", "data1"))
print(set("key2", "data2"))
#print(set("key3", "data3"))
print(delete("key3"))
print(dataset)
