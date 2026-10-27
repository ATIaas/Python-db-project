# This is a subset of functions defined for the class BaseDBClass

# Should probably make a key and value validation function



def set(S, key:str, data:str) -> str:

    S._validate_pair(key, data) ;

    key = S._hash_func.encrypt(key)

    with open(S._file_path, 'a', encoding=S._encoding) as file:
        file.write(key + ":" + data + "\r\n")

    if key in S._dictDB.keys():
        S._dictDB[key] = data
        return "Already exists"

    S._dictDB[key] = data
    return "saved " + "\"" + data + "\"" + " in key:" + key


def get(S, key:str) -> str:
    S._validate_key(key) ;

    key = S._hash_func.encrypt(key)
    return S._dictDB.get(key,"Key_not_found!")


def delete(S, key:str) -> str:
    S._validate_key(key) ;

    key = S._hash_func.encrypt(key)

    if key in S._dictDB.keys():
        temp:str = S._dictDB.pop(key)

        with open(S._file_path, 'a', encoding=S._encoding) as file:
            file.write("?" + key + "\r\n")

        return ("Deleted data: " + temp)
    else:
        raise KeyError("Key not in use")

