import io

class loadedDB:
    """
    Is the base class for the virtualization of the db
    Mainly a way to separate the virtual storage from the file management

    In this case the data will be stored with strings

    :Suffix: LDB
    """

    def __init__(self, size: int):
        self.size = size
        self.table = {}

    # Public functions

    def get(self, key: int):
        key = key % self.size
        return self.table[key]

    # Protected functions

    def _remove(self, key: int):
        key = key % self.size
        self.table.pop(key)

    def _insert(self, key: int, value: str):
        key = key % self.size
        self.table[key] = value
