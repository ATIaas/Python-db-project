from src.Clases.BaseHashFunc import BaseHashClass

# modular function creation
from src.Clases.BaseDBClass_modules.basic_interaction import set, get, delete
from src.Clases.BaseDBClass_modules.consolidate import consolidate



# Constants declaration
# Could probably make this a .env getter
BaseDBClass__FLAGS_BINARY_FILE_ACCEPT = False
BaseDBClass__ACCEPTED_ENCODINGS = ['utf-8','utf-16','utf-32']

class BaseDBClass:
    """
    Base class example for the DB project is literally a restructure
    SUFFIX: BDB
    """

    #self vars
    _dictDB:dict[str,str] = {}
    _file_path:str
    _hash_func:BaseHashClass
    _encoding:str


    # INIT block


    # further file options and special flags can be added
    def file_compatability_check(self, file_path:str)->bool:
        if file_path.endswith('.txt'):
            return True

        return False



    def __init__(self,path:str, **kwargs):
        """
        :param path:str = is the name of the file or the absolute path of the file
        :param kwargs:
        -- hash_func:BaseHashClass = The hashing function for the key default is the blank case
        |default[hash_func]=BaseHashClass()
        -- encoding:str = is the encoding for the key default is the blank case
        |default[encoding]=utf-8
        |constrains[encoding]=in ["utf-8","utf-16","utf-32"]
        """

        if not self.file_compatability_check(path):
            raise TypeError('The file path provided is not valid for this DB class')

        self._hash_func = kwargs.get('hash_func',BaseHashClass())

        if type(self._hash_func) != BaseHashClass:
            raise TypeError('The hashing function provided is not interchangeable with BaseHashClass')


        self._encoding = kwargs.get('encoding','utf-8')

        if type(self._encoding) != str:
            raise TypeError('The encoding provided is not interchangeable with BaseHashClass')
        if self._encoding not in BaseDBClass__ACCEPTED_ENCODINGS:
            raise TypeError('The encoding provided is not accepted for this DB class')


        # Create the file in case it does not exist
        open(path,'a').close()

        self._file_path = path

        self._initialize_the_DB()


    def _initialize_the_DB(self):

        with open(self._file_path,'r', encoding=self._encoding) as file:
            for line in file:
                line = line.rstrip("\n")

                if line[0] == '?':
                    line = line.lstrip("?")
                    key = line
                    del self._dictDB[key]

                elif line.find(':') == -1:
                    pass #ignores wrong lines

                else:
                    key, data = line.split(":")
                    self._dictDB[key] = data

    #-------------------------------------------------------------

    def _validate_key(self, key:str)->None:
        if key == "":
            raise ValueError("key cannot be empty")

        if ":" in key:
            raise ValueError("key cannot contain \":\"")

        if key.startswith("?"):
            raise ValueError("key cannot start with \"?\"")

        if "\n" in key:
            raise ValueError("key and data cannot contain line breaks")


    def _validate_value(self, value:str)->None:
        if value == "":
            raise ValueError("value cannot be empty")
        if "\n" in value:
            raise ValueError("key and data cannot contain line breaks")


    def _validate_pair(self, key:str, value:str)->None:
        self._validate_key(key)
        self._validate_value(value)



    #-------------------------------------------------------------

    # Getters

    @property
    def file_path(self)->str:
        return self._file_path


    @property
    def hash_func(self)->BaseHashClass:
        return self._hash_func


    @property
    def encoding(self)->str:
        return self._encoding


    @property
    def dict(self)->dict[str,str]:
        return self._dictDB

    #----------------------------------------------------------------

    # Not sure that setters are completely necessary



# END OF CLASS

# Man do I prefer even fucking cpp when it comes to fragmentalized class function declarations over this BS

BaseDBClass.set = set ; del set
BaseDBClass.get = get ; del get
BaseDBClass.delete = delete ; del delete
BaseDBClass.consolidate = consolidate ; del consolidate


