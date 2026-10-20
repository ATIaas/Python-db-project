from dataclasses import dataclass


@dataclass
class lineAction:
    """
    This is basically a struct to define the lineActions class used to reduce lock waits between threads

    Is basically a struct, python does not have structs
    """
    order: str = ""
    key: str = ""
    hash: int = -1

    value: str = ""
    is_full_chunk: bool = False

    def __init__(self): pass ;

    @classmethod
    def create_set(cls, hash_: int, value_: str, key_: str = ""):
        """
        Non-mandatory params are for methods that interact with the file as writers

        """
        cls.order = "set"
        cls.key = key_
        cls.hash = hash_
        cls.value = value_



    @classmethod
    def create_unset(cls, hash_: int, key_: str = ""):
        """
        Non-mandatory params are for methods that interact with the file as writers

        """
        cls.order = "unset"
        cls.key = key_
        cls.hash = hash_

    @classmethod
    def create_first(cls, value_: str = "", full_chunk: bool = False):
        cls.order = "first"
        cls.value = value_
        cls.is_full_chunk = full_chunk

    @classmethod
    def create_last(cls, value_: str = ""):
        cls.order = "last"
        cls.value = value_

