class InvalidCommand(SyntaxError):
    def __init__(self, message: str) -> None:
        super(InvalidCommand, self).__init__(message)


class FileOperationError(IOError):
    def __init__(self, message: str) -> None:
        super(FileOperationError, self).__init__(message)


class CommonException(Exception):
    def __init__(self, message: str) -> None:
        super(CommonException, self).__init__(message)
