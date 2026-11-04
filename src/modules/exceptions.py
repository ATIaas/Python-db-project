class DBError(Exception):
    def __init__(self, message:str = "Something went wrong with the database", code:str = "DB") -> None:
        self.message:str = message
        self.code:str = code
        super().__init__(message)
        
class SpaceError(DBError):
    def __init__(self) -> None:
        message:str = "Not enough space in memory for file"
        code:str = "SPACE"
        super().__init__(message, code)

class TSpaceError(DBError):
    def __init__(self) -> None:
        message:str = "Not enough space in memory for temp file"
        code:str = "TSPACE"
        super().__init__(message, code)

class FileError(DBError):
    def __init__(self) -> None:
        message:str = "File not found or not readable"
        code:str = "FILE"
        super().__init__(message, code)


class AccessError(DBError):
    def __init__(self) -> None:
        message:str = "Unable to access file"
        code:str = "ACCESS"
        super().__init__(message, code)


class DBKeyError(DBError):
    def __init__(self, message:str = "DB key error") -> None:
        code:str = "KEY"
        super().__init__(message, code)

class DBValueError(DBError):
    def __init__(self, message:str = "DB value error") -> None:
        code:str = "VALUE"
        super().__init__(message, code)
