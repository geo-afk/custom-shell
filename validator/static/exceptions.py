"""
This module defines custom exceptions for command validation,
file operations, and common error scenarios. These exceptions
provide clear feedback for invalid commands or operations.
"""

class CustomBaseException(Exception):
    """
    Base class for all custom exceptions in this module.
    """
    def __init__(self, message: str) -> None:
        super().__init__(message)


class InvalidCommand(CustomBaseException):
    """
    Exception raised when an invalid command is encountered.
    """
    pass


class FileOperationError(CustomBaseException):
    """
    Exception raised for an invalid file operation.
    """
    pass


class FileAccessError(CustomBaseException):
    """
    Exception raised for an invalid file/folder access operation.
    """
    pass


class DirectoryManagementError(CustomBaseException):
    """
    Exception raised for an invalid directory management command.
    """
    pass


class RedirectionError(CustomBaseException):
    """
    Exception raised for an invalid directory management command.
    """
    pass
