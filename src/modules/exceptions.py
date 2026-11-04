
class SpaceError(Exception):
    def __init__(self) -> None:
        self.message = "Not enough space in memory for file"
        self.code = "SPACE"
        super().__init__(self.message)

class TSpaceError(Exception):
    def __init__(self) -> None:
        self.message = "Not enough space in memory for temp file"
        self.code = "TSPACE"
        super().__init__(self.message)

class FileError(Exception):
    def __init__(self) -> None:
        self.message = "File not found or not readable"
        self.code = "FILE"
        super().__init__(self.message)


class AccessError(Exception):
    def __init__(self) -> None:
        self.message = "Unable to access file"
        self.code = "ACCESS"
        super().__init__(self.message)


class DBKeyError(Exception):
    def __init__(self, message:str = "DB key error") -> None:
        self.message = message
        self.code = "ACCESS"
        super().__init__(self.message)

class DBValueError(Exception):
    def __init__(self, message:str = "DB value error") -> None:
        self.message = message
        self.code = "ACCESS"
        super().__init__(self.message)



