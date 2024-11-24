from typing import List

from validator.static.constant_types import (
    FileOperation,
    FilePermission,
    DirectoryOperation
)

from SyntaxShift.directory_handler import DirectoryManagementHandler
from SyntaxShift.file_access_handler import FileAccessHandler
from SyntaxShift.file_operation_handler import FileOperationHandler

from validator.static.exceptions import RedirectionError
from validator.static.constant_types import FILE_OPERATIONS, FILE_PERMISSIONS, DIRECTORY_OPERATIONS, Platform

class RedirectHandler:
    """
    Handles and validates redirection operations in the command-line input.
    """


    def __init__(self, command: List[str], operating_system: Platform, redirect: str):
        """
        Initialize the RedirectHandler.

        Args:
            command (List[str]): The user command to handle.
            operating_system (Platform): The operating system for system-specific operations.
            redirect (str): The type of redirection ('<' or '>').
        """
        self.commands = command
        self.operating_system = operating_system
        self.redirect = redirect


    def check_redirect_operation(self):
        """
        Check and validate the redirection operation based on the redirection type.

        Returns:
            The result of the corresponding redirection operation if valid.

        Raises:
            RedirectionError: If the redirection command is invalid.
        """
        command_type = self.commands[0]


        if self.redirect == "<":
            return self.redirect_into(command_type)

        elif self.redirect == ">":
            return self.redirect_output(command_type)


        raise RedirectionError("Invalid Redirection Command.... {self.command}")

    def redirect_output(self, command_type):
        """
        Handle the '>' redirection (output) for file operations, file permissions, and directory operations.

        Args:
            command_type (str): The type of operation being performed.

        Returns:
            Result of the operation (file operation, file access, or directory management).
        """
        index = self.commands.index(">")
        command = self.commands[:index]

        if command_type in FileOperation:

            rename = None
            if command_type == "rename":
                rename = input("Enter new filename: ")
            operation = FileOperationHandler(command, self.operating_system)
            return operation.check_file_operation(rename)

        elif command_type in FilePermission:
            print("FIle Permission")
            operation = FileAccessHandler(command, self.operating_system)
            return operation.check_file_access()

        elif command_type in DirectoryOperation:
            operation = DirectoryManagementHandler(command, self.operating_system)
            return  operation.make_directory_command()

        return None

    def redirect_into(self, command_type:str):
        """
        Handle the '<' redirection (input) for file operations, file permissions, and directory operations.

        Args:
            command_type (str): The type of operation being performed.

        Returns:
            The corresponding operation handler based on the command type.
        """
        operation = None
        if command_type in FileOperation:
            operation = FILE_OPERATIONS[command_type][self.operating_system]

        elif command_type in FilePermission:
            operation = FILE_PERMISSIONS[command_type][self.operating_system]

        elif command_type in DirectoryOperation:
            operation = DIRECTORY_OPERATIONS[command_type][self.operating_system]

        return operation
