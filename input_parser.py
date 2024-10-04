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



from typing import List
from static.exceptions import InvalidCommand
from static.constant_types import FileOperation, VALID_EXTENSIONS, PIPES


class InputParser:
    def __init__(self, user_input: str) -> None:
        self.user_input: str = user_input.strip()
        self.VALID_OPERATIONS: List[str] = self.get_valid_operations()
        self.parsed_inputs: List[str] = self.split_and_lowercase_user_input()

    def split_and_lowercase_user_input(self) -> List[str]:
        """
            this function first splits the user input string into at max 6
            words and place each of them into a list[str], then after is runs
            through the list of words and check if it has valid commands which
            it then removes the command and adds the lowercase of that removed
            command.
            :return: list of operations
        """
        input_list: List[str] = self.user_input.split(" ", maxsplit=6)

        for index, command in enumerate(input_list):
            if command in self.VALID_OPERATIONS:
                input_list.pop(index)
                input_list.insert(index, command.lower())

        return input_list

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

        raise InvalidCommand(f"Invalid..! Command '{self.user_input}' is not valid")


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
        if operation not in self.VALID_OPERATIONS:
            return False

        if len(self.parsed_inputs) < 2 and operation != "help":
            return False

        if operation == "help":
            return self.valid_help_input()

        if len(self.parsed_inputs) == 2:
            return self.valid_file_extension(self.parsed_inputs[1])

        if len(self.parsed_inputs) > 2:
            if self.parsed_inputs[3] not in PIPES or not self.valid_piped_operations(
                self.parsed_inputs[4:]
            ):
                return False

        return True

    def valid_help_input(self):
        """
            if the user request to use the help operation, this function is called to validate
            the user input for the help command, it checks id the user is requesting
            specific help for a supported command or the general help where list all
            supported commands.
            :return: True or False.
        """
        if len(self.parsed_inputs) == 1:
            return True

        return len(self.parsed_inputs) == 2 and self.parsed_inputs[1] in FileOperation

    def valid_piped_operations(self, piped_operations: list[str]) -> bool:
        """
            if the user opted for a piped command then this function is used
             to check the right half of the piped input to see if it is valid.
            :param piped_operations: operations on the right half of command
            :return: Function: is_operation_valid(...,...) to validate
        """
        return self.is_operation_valid(piped_operations[0], piped_operations[1:])

    def is_operation_valid(self, operation: str, args: list[str]) -> bool:
        """
            Validates the operation and its arguments.
            This function checks whether both the operation and the provided arguments are valid.
            For example, if the user wants to create a file, the function checks if the operation
            is 'create' and the arguments include a valid file extension (e.g., 'filename.txt').

            :param operation: The command that the user wants to execute (e.g., 'create').
            :param args: The arguments for the command (e.g., the filename in 'create <filename>').
            :return: True if both the operation and its arguments are valid.
        """

        operations: list[str] = self.VALID_OPERATIONS

        if operation not in operations:
            return False

        if len(args) == 1 and not self.valid_file_extension(args[0]):
            return False

        return True

    @staticmethod
    def get_valid_operations() -> List[str]:
        """
            function is used to retrieve the operations
            the program support
            operations is retrieved from the enum: 'FileOperation'
            from 'FileOperation' it retrieves the names which are essentially
            the variables in that enum and because they are upper
            case they are needed to be lowercase
            and 'help' operation will be added as that is not in
            the 'FileOperation' enum, but it is a
            valid operation.
            :return: A list of valid operations.
        """
        operations: list[str] = [operation.value for operation in FileOperation]
        operations.append("help")

        return operations

    @staticmethod
    def valid_file_extension(file: str) -> bool:
        """
            function is used check if the inputted file from the user
            has a supported file extension
        """
        file_extension = file.split(".")[-1]
        return f".{file_extension}" in VALID_EXTENSIONS
