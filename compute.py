"""
    This module is used to translate the commands of the user
    into command line argument and executing them depending on the user
    operating system.
    the program works by figuring out if the requested operations
    is a piped command or non-piped command
    and executing them accordingly,
    the program also check if operation requested is 'delete or rename'
    operation, if:
    delete then it checks if the file exists first before deleting any file,
    rename: it also checks if the file already exists before doing rename operation

"""


from typing import List, Optional
import subprocess
import os
from static.constant_types import (
    FileOperation,
    FILE_OPERATIONS,
    Platform,
    VALID_EXTENSIONS,
    PIPES,
)
from static.exceptions import InvalidCommand, FileOperationError


class ComputeOperations:
    def __init__(self, command_args: List[str], operating_system: Platform) -> None:
        self.command_args = command_args
        self.platform = operating_system


    def split_piped_commands(self) -> tuple[None | List[str], None | List[str]]:
        for i, arg in enumerate(self.command_args):
            if arg in PIPES:
                return self.command_args[:i], self.command_args[i + 1 :]
        return None, None


    def prepare_rename_command(self, old_filename: str) -> List[str]:
        if not self.file_exists(old_filename):
            raise FileOperationError(f"Invalid rename operation: '{old_filename}' does not exist")
        else:
            new_filename = input("Enter new filename: ")

            if not self.is_valid_file_extension(new_filename):
                raise InvalidCommand(
                    f"Invalid.. Supported extensions are: {', '.join(VALID_EXTENSIONS)}"
                )
            if self.file_exists(new_filename):
                raise FileOperationError(f"File '{new_filename}' already exists")

            operation = FileOperation("rename")
        return FILE_OPERATIONS[operation][self.platform] + [old_filename, new_filename]

    def validate_delete_operation(self, filename: str) -> None:
        if not self.file_exists(filename):
            raise FileOperationError(f"Invalid delete operation: '{filename}' does not exist")

    def is_command_piped(self) -> bool:
        return any(pipe in self.command_args for pipe in PIPES)

    def execute_operation(self) -> None:
        if not self.is_command_piped():
            self.execute_single_operation()
        else:
            self.execute_piped_operation()

    def execute_single_operation(self) -> None:
        operation = FileOperation(self.command_args[0].lower())
        command = FILE_OPERATIONS[operation][self.platform] + [self.command_args[1]]

        if operation == FileOperation.DELETE:
            self.validate_delete_operation(self.command_args[1])
        elif operation == FileOperation.RENAME:
            command = self.prepare_rename_command(self.command_args[1])

        self.execute_command(command)

    def execute_piped_operation(self) -> None:
        first_command, second_command = self.split_piped_commands()

        if not first_command or not second_command:
            raise InvalidCommand("Invalid piped command")

        first_operation = FileOperation(first_command[0].lower())
        second_operation = FileOperation(second_command[0].lower())

        first_cmd = FILE_OPERATIONS[first_operation][self.platform] + first_command[1:]
        second_cmd = (
            FILE_OPERATIONS[second_operation][self.platform] + second_command[1:]
        )

        self.execute_piped_command(first_cmd, second_cmd)

    @staticmethod
    def execute_piped_command(first_command: List[str], second_command: List[str]) -> None:
        with subprocess.Popen(first_command, stdout=subprocess.PIPE) as first_process:
            with subprocess.Popen(
                    second_command, stdin=first_process.stdout, stdout=subprocess.PIPE
            ) as piped_process:
                if first_process.stdout:
                    first_process.stdout.close()
                output, _ = piped_process.communicate()
                print(output.decode("utf-8"))

    @staticmethod
    def execute_command(command: List[str]) -> Optional[subprocess.CompletedProcess]:
        try:
            return subprocess.run(
                args=command, check=True, stdout=subprocess.PIPE, text=True
            )
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
            print(f"Command output: {e.stdout}")
        return None


    @staticmethod
    def file_exists(filename: str) -> bool:
        return os.path.exists(filename)

    @staticmethod
    def is_valid_file_extension(file: str) -> bool:
        file_extension = os.path.splitext(file)[1]
        return file_extension in VALID_EXTENSIONS
