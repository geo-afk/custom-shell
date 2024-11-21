"""
    This module is responsible for parsing user input strings. It performs the following steps:

    1. Strips any leading whitespace from the input string.
    2. Splits the input string into individual words.
    3. Checks for the presence of operation instructions (e.g., 'create', 'delete') in the string.
       If found, ensures they are in lowercase for case-insensitive comparison.
    4. Validates the parsed input to determine if the operation is a valid system command.

    The validation process:
    - Verifies if the first word in the parsed string corresponds to a valid operation.
    - Checks if the user is requesting help; if not, determines whether the operation is
     a valid single command or a piped command.

    If all operations are valid, the module returns the parsed list of words. Otherwise,
    it raises an `InvalidCommand` exception.
"""



import shlex
from typing import List

from validator.redirect_validator import RedirectValidator

from validator.directory_management_validator import DirectoryManagementValidator
from validator.file_operation_validator import FileOperationValidator
from validator.file_access_validator import FileAccessValidator
from validator.piped_command import PipedCommandValidator
from validator.static.exceptions import InvalidCommand
from validator.help_validator import HelpValidator
from validator.validator import Validator

class InputParser:
    def __init__(self, user_input: str) -> None:
        self.user_input: str = user_input.strip()
        self.valid = Validator()
        self.parsed_inputs: List[str] = self.split_and_lowercase_user_input()

    def split_and_lowercase_user_input(self) -> List[str]:
        """
            this function first splits the user input string into at max 6
            words and place each of them into a list[str], then after is runs
            through the list of words and check if it has valid commands which
            it then removes the command and adds the lowercase of that removed
            command.
            return: list of operations
        """
        input_list: List[str] = shlex.split(self.user_input)
        return [command.lower() if command in self.valid.get_valid_operations() else command for command in input_list]


    def retrieved_parsed_input(self):
        """
            functions is called to retrieve parsed input, it calls 'is_parsed_input_valid'
            to validate the list of operations if returns true, then
            the function returns
            if it is not it throws:
            :return: list of operations
            :raise: InvalidCommand
        """
        if self.is_parsed_input_valid():
            return self.parsed_inputs

        raise InvalidCommand(f"Invalid..! Command: '{self.user_input}' is not valid")


    def is_parsed_input_valid(self) -> bool:
        """
            Validates the parsed input from the user to ensure it
            conforms to a recognized command structure.
            This function performs the following checks:

            1. Confirms that the parsed input is not empty.
            2. Validates that the first word in the parsed
            input matches a valid operation.
            3. If the operation is "help", checks if the input
             requests general help or help for a specific valid command.
            4. Ensures that other operations have the correct number of arguments.
            5. For piped commands, it verifies that the right-hand
            side of the pipe contains valid operations.
            :return: True if the parsed input is valid, otherwise False.
        """
        if not self.parsed_inputs:
            return False

        operation = self.parsed_inputs[0]
        if operation not in self.valid.get_valid_operations():
            return False

        elif "|" in self.parsed_inputs:
            piped_commands = PipedCommandValidator(self.parsed_inputs)
            return piped_commands.valid_piped_operations()


        elif any(symbol in self.parsed_inputs for symbol in ['<', '>']):
            return RedirectValidator(self.parsed_inputs).validate()

        elif operation in ["modify", "list"]:
            file_access_valid = FileAccessValidator(self.parsed_inputs)
            return file_access_valid.validate()

        elif operation == "help":
            help_valid: HelpValidator = HelpValidator(self.parsed_inputs)
            return help_valid.valid_help_input()

        elif operation in ["create", "delete", "rename"]:
                file_operation_valid = FileOperationValidator(self.parsed_inputs[1:])
                return file_operation_valid.is_operation_valid()

        elif operation in ["change", "remove", "make", "pwd"]:
            directory_valid = DirectoryManagementValidator(self.parsed_inputs)
            return  directory_valid.validate()


        return False