



class BaseHashClass:
    """
    Base class example for the DB project is literally an override ,
    Reason for it being a class is in case of the use of more complex hashing algorithms
    SUFFIX: HASH
    """

    def __init__(self): pass;


    def encrypt(self, key:str):
        """
        :param key: what to encrypt
        :return: For the base case same as key
        Returns are not typed for base classes for Override ease
        """
        return key

