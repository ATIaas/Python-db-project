import io
import threading
import multiprocessing as mp
from platform import release

from threading import Thread, Lock

from loadedDB import loadedDB

from hashFuncs import hashFunc

from lineAction import lineAction


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
        :keyword dict_size: the size of the internal map/dictionary for DB in memory store : int = 1000
        :keyword encoding: the encoding of the file : str = 'utf-32',CONSTRAINED by ACCEPTED_ENCODINGS
        :keyword concurrent_threads: the number of concurrent threads for async file reading and consolidation : int = 10
        :keyword thread_buffer: the buffer size to be interpreted by each thread in characters : int = 1024, CONSTRAIN at least 256
        """
        self.filename = filename

        self.dict_size = kwargs.get('dict_size', 1000)
        if type(self.dict_size) != int :
            raise TypeError('the size of the dictionary must be an integer')


        self.encoding = kwargs.get('encoding', 'utf-32')
        if type(self.encoding) != str and self.encoding not in ACCEPTED_ENCODINGS:
            raise TypeError('the file encoding system is not recognized')


        self.hashing_func = kwargs.get('hashing_func', hashFunc())
        if type(self.hashing_func) != hashFunc :
            raise TypeError('the hashing function is not derived from the base class hashFunc')


        self.concurrent_threads = kwargs.get('concurrent_threads', 10)
        if type(self.concurrent_threads) != int :
            raise TypeError('the number of concurrent threads must be an integer')


        self.thread_buffer = kwargs.get('thread_buffer', 1024)
        if type(self.thread_buffer) != int :
            raise TypeError('the buffer size to be interpreted by each thread must be an integer')
        elif self.thread_buffer < 256 :
            # trust me less than this and we are just putting the memory to work
            raise ValueError('a buffer of less than 256 characters is a waste of threading')


        self.loadedDB = loadedDB(self.dict_size)

        self.__file_data_load()


# General functions
    def __line_parser(self, line: str)->lineAction:
        line = line.rstrip("\n")
        if line == "":
            return lineAction() # dud return

        if line[0] == '?':
            line = line.lstrip("?")
            ret = lineAction.create_unset(self.hashing_func(line),line)

        else:
            split_point = line.find(":")

            if split_point != -1:
                key = line[0:split_point]
                value = line[split_point + 1:]
                ret = lineAction.create_set(self.hashing_func(key),value, key)
                return ret

        return lineAction() # dud return



    def __chunk_parser(self, chunk: str)->list[lineAction]:
        """
        :param chunk: the chunk to be parsed
        :return: is a list of items of the order class
        """
        ret = []
        counter = 0
        split_point = chunk.find("/n")

        while split_point != -1:
            if counter == 0:
                data = chunk[:split_point]
                chunk = chunk[split_point + 1:]
                if chunk != "":
                    ret.append(lineAction.create_first(data,chunk == ""))
            else:
                data = chunk[:split_point]
                chunk = chunk[split_point + 1:]
                potential = self.__line_parser(data)
                if potential.order != "":
                    ret.append(potential)

            counter += 1
            split_point = chunk.find("/n")

        if chunk != "":
            ret.append(lineAction.create_last(chunk))

        return ret


    __chunk_counter = 0
    __current_file_io = None # set to open(filename, 'r', encoding self.encoding)
    def __thread_chunk_getter(self)->dict:
        """
        REQUIREMENT to initialize the self.__chunk_counter at 0 before calling this
        REQUIREMENT to initialize the self.__current_file_io as a file with the reading permission

        :returns {"n":chunk_num, "data":chunk}
        REMINDER Python does not read EOF's so make sure to end threads when they get a empty string.
        """
        self.__file_cond.acquire()

        ret:dict = { "n":self.__chunk_counter, "data":self.__current_file_io.read(self.thread_buffer) }
        self.__chunk_counter += 1


        self.__file_cond.release()



        return ret



    def __leading_tail_procesing(self, action:lineAction, chunk_n)->None:
        if (chunk_n -1) in self.__completed_chunks:
            if (chunk_n - 1) in self.__leading_tail.keys():
                pass
            else:
                pass
        else:
            self.__leading_tail[chunk_n] = [action.value, "T" if action.is_full_chunk else  "F" ]



    def __ending_tail_procesing(self, action:lineAction, chunk_n)->None:
        pass



    def __implement_lineAction(self, action:lineAction, chunk_n:int)->None:
        match action.order:
            case "first":
                self.__leading_tail_procesing(action, chunk_n)
            case "last":
                self.__ending_tail_procesing(action, chunk_n)
            case _:
                key = self.hashing_func(action.key)
                if not (key in self.__actions_taken.keys() and self.__actions_taken[
                    key] > chunk_n):  # this is to not overide future actions
                    match action.order:
                        case "set":
                            self.loadedDB._insert(key, action.value)
                            self.__actions_taken[key] = chunk_n
                        case "unset":
                            self.loadedDB._delete(key)
                            self.__actions_taken[key] = chunk_n



    def __thread_action_maker(self, actions:list[lineAction], chunk_n:int )->None:

        self.__actions_cond.acquire()

        for action in actions:
            self.__thread_action_maker(action, chunk_n);


        self.__action_cond.release()



        return









# Data Loading





    def __dataload_thread_func(self):
        current_dict = self.__thread_chunk_getter();
        while current_dict.get("data") != "":

            current_dict = self.__thread_chunk_getter()
            actions = self.__chunk_parser(current_dict["data"])
            self.__thread_action_maker(actions, current_dict["n"])




    def __dataload_thread_orchestrator(self)->None:
        self.__chunk_counter:int = 0
        self.__current_file_io= open(self.filename, "r", encoding=self.encoding) # typing does not work
        self.__actions_taken:dict[int, int] = {} #key, last chunk N to do action on it

        # both of those will be in the form {chunk_num:{"data":... , "full_chunk":"1/0"<-basically bool}}
        self.__leading_tail:dict[int,list[str]] = {}
        self.__ending_tail: dict[int, list[str]] = {}

        self.__completed_chunks:set[int] = set() #set of completed chunks

        self.__file_cond = mp.Condition()
        self.__action_cond = mp.Condition()





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