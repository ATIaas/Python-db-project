# This is a subset of functions defined for the class BaseDBClass

def set(S, key:str, data:str) -> str:

    if key == "":
        raise ValueError("key cannot be empty")

    if ":" in key:
        raise ValueError("key cannot contain \":\"")

    if key.startswith("?"):
        raise ValueError("key cannot start with \"?\"")

    if "\n" in key or "\n" in data:
        raise ValueError("key and data cannot contain line breaks")

    key = S._hash_func.encrypt(key)

    with open(S._file_path, 'a', encoding=S._encoding) as file:
        file.write(key + ":" + data + "\r\n")

    if key in S._dictDB.keys():
        S._dictDB[key] = data
        return "Already exists"

    S._dictDB[key] = data
    return "saved " + "\"" + data + "\"" + " in key:" + key


def get(S, key:str) -> str:
    if key == "":
        raise ValueError("key cannot be empty")

    if ":" in key:
        raise ValueError("key cannot contain \":\"")

    if key.startswith("?"):
        raise ValueError("key cannot start with \"?\"")

    if "\n" in key:
        raise ValueError("key and data cannot contain line breaks")

    key = S._hash_func.encrypt(key)
    return S._dictDB.get(key,"Key_not_found!")


def delete(S, key:str) -> str:
    if key == "":
        raise ValueError("key cannot be empty")

    if ":" in key:
        raise ValueError("key cannot contain \":\"")

    if key.startswith("?"):
        raise ValueError("key cannot start with \"?\"")

    if "\n" in key:
        raise ValueError("key and data cannot contain line breaks")

    key = S._hash_func.encrypt(key)

    if key in S._dictDB.keys():
        temp:str = S._dictDB.pop(key)

        with open(S._file_path, 'a', encoding=S._encoding) as file:
            file.write("?" + key + "\r\n")

        return ("Deleted data: " + temp)
    else:
        raise KeyError("Key not in use")

