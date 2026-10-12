import io

from loadedDB import loadedDB

from hashFuncs import hashingFunction

ACCEPTED_ENCODINGS = ['utf-32', 'utf-16', 'utf-8', 'ASCII']

class utf32FileHashDB:
    """
    This is the base class associated with all inward DB calls at the low level
    It is a pseudo orchestrator for the virtualization of the line by line db

    :Suffix: FHDB
    """

    def __init__(self, filename: str, **kwargs):
        """
        :param filename: the name of the associated file
        :keyword dict_size: the size of the internal map/dictionary for DB in memory store : int = 100
        :keyword encoding: the encoding of the file : str = 'utf-32',CONSTRAINED by ACCEPTED_ENCODINGS
        :keyword concurrent_threads: the number of concurrent threads for async file reading and consolidation : int = 10
        :keyword thread_buffer: the buffer size to be interpreted by each thread in bytes : int = 4000, CONSTRAIN at least 1024
        """
        self.filename = filename

        self.dict_size = kwargs.get('dict_size', 100)
        if type(self.dict_size) != int :
            raise TypeError('the size of the dictionary must be an integer')


        self.encoding = kwargs.get('encoding', 'utf-32')
        if type(self.encoding) != str and self.encoding not in ACCEPTED_ENCODINGS:
            raise TypeError('the file encoding system is not recognized')\


        self.hashing_func = kwargs.get('hashing_func', hashingFunction(self.encoding))
        if type(self.hashing_func) != hashingFunction :
            raise TypeError('the hashing function is not derived from the base class hashingFunction')


        self.concurrent_threads = kwargs.get('concurrent_threads', 10)
        if type(self.concurrent_threads) != int :
            raise TypeError('the number of concurrent threads must be an integer')


        self.thread_buffer = kwargs.get('thread_buffer', 4000)
        if type(self.thread_buffer) != int :
            raise TypeError('the buffer size to be interpreted by each thread must be an integer')
        elif self.thread_buffer < 1024 :
            # trust me less than this and we are just putting the memory to work
            raise ValueError('a buffer of less than 1024 bytes is a waste of threading')


        self.loadedDB = loadedDB(self.dict_size)

        self.__file_data_load()


    def __file_data_load(self):
        pass



    def new_entry(self, key: str, value:str):
        hash = self.hashing_func(key)
        self.loadedDB._insert(hash, value)

        with open(self.filename, 'ab', encoding=self.encoding) as f:
            amendum = key
            amendum += ":"
            amendum += value
            amendum += "\r\n"
            amendum = amendum.encode(self.encoding)
            f.write(amendum)


    def remove_entry(self, key: str):
        hash = key.encode(self.encoding)
        self.loadedDB._remove(hash)

        with open(self.filename, 'ab', encoding=self.encoding) as f:
            amendum = "?"
            amendum += key
            amendum += "\r\n"
            amendum = amendum.encode(self.encoding)
            f.write(amendum)


    def _consolidate_file(self): pass ;