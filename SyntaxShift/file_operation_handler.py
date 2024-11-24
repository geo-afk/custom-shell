from os import path
import logging

from validator.static.constant_types import FileOperation
from validator.static.constant_types import Platform
from validator.static.constant_types import FILE_OPERATIONS
from validator.static.constant_types import VALID_EXTENSIONS
from validator.static.exceptions import FileOperationError


logging.basicConfig(level=logging.INFO)


class FileOperationHandler:
    """
    Handles file operations like create, delete, and rename for specific platforms.

    Attributes:
        command (list[str]): List containing operation and filename.
        operating_system (str): Current operating system.
    """

    def __init__(self, command: list[str], operating_system: Platform):
        """
        Initialize the file operation handler.

        Args:
            command (list[str]): Operation and filename.
            operating_system (str): Operating system.
        """
        if not command or len(command) < 2:
            raise ValueError("Invalid command. Must include operation and filename.")
        self.command = command
        self.operating_system = operating_system



    def check_file_operation(self, new_filename: str = None):
        operation = FileOperation(self.command[0])
        self.validate_operation(operation, self.command[1])

        command = FILE_OPERATIONS[operation][self.operating_system] + [self.command[1]]

        if operation == FileOperation.RENAME:
            if not new_filename:
                raise ValueError("New filename is required for rename operation.")
            return self.handle_rename(command, new_filename)

        return command




    def handle_rename(self, command, new_filename: str):
        file_extension = path.splitext(new_filename)[1]

        if not file_extension in VALID_EXTENSIONS:
            raise FileOperationError(f"Invalid file extension for '{new_filename}'.")

        if self.file_exists(new_filename):
            raise FileOperationError(f"File with name '{new_filename}' already exists.")

        return command + [new_filename]




    def validate_operation(self, operation, filename):
        logging.info(f"Validating operation '{operation}' for file '{filename}'.")

        file_exists = self.file_exists(filename)

        if operation == FileOperation.DELETE and not file_exists:
            raise FileOperationError(f"Failed to delete: '{filename}', file does not exist.")

        if operation == FileOperation.CREATE and file_exists:
            raise FileOperationError(f"Cannot create file: '{filename}', file already exists.")

        if operation == FileOperation.RENAME and not file_exists:
            raise FileOperationError(f"Cannot rename '{filename}', file does not exist.")

    @staticmethod
    def file_exists(filename: str) -> bool:
        return path.exists(filename)