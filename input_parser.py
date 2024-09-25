from typing import List
from static.exceptions import InvalidCommand
from static.constant_types import FileOperation, VALID_EXTENSIONS, PIPES


class InputParserAndValidator:
    def __init__(self, user_input: str) -> None:
        self.user_input: str = user_input.strip()
        self.parsed_inputs: List[str] = self.split_and_lowercase_user_input()

    def split_and_lowercase_user_input(self) -> List[str]:
        input_list: List[str] = self.user_input.split(" ", maxsplit=6)

        for i in range(len(input_list)):
            command = input_list[i].lower()
            if command in self.get_valid_operations():
                input_list.pop(i)
                input_list.insert(i, command)

        return input_list

    def retrieved_parsed_input(self):
        if self.is_parsed_input_valid():
            return self.parsed_inputs

        raise InvalidCommand(f"Invalid..! Command '{self.user_input}' is not valid")

    def is_parsed_input_valid(self) -> bool:
        if not self.parsed_inputs:
            return False

        operation = self.parsed_inputs[0]
        if operation not in self.get_valid_operations():
            return False

        if len(self.parsed_inputs) < 2 and operation != "help":
            return False

        if operation == "help":
            return self.valid_help_input()

        elif len(self.parsed_inputs) == 2:
            return self.valid_file_extension(self.parsed_inputs[1])

        elif len(self.parsed_inputs) > 2:
            if self.parsed_inputs[3] not in PIPES or not self.valid_piped_operations(
                self.parsed_inputs[4:]
            ):
                return False

        return True

    def valid_help_input(self):
        if len(self.parsed_inputs) == 1:
            return True

        if (
            len(self.parsed_inputs) == 2
            and self.parsed_inputs[1].upper() in FileOperation._member_names_
        ):
            return True
        return False

    def valid_piped_operations(self, piped_operations: list[str]) -> bool:
        return self.is_operation_valid(piped_operations[0], piped_operations[1:])

    def is_operation_valid(self, operation: str, args: list[str]) -> bool:
        operations: list[str] = self.get_valid_operations()

        if operation not in operations:
            return False

        if len(args) == 1 and not self.valid_file_extension(args[0]):
            return False

        return True

    @staticmethod
    def get_valid_operations() -> List[str]:
        operations: list[str] = FileOperation._member_names_.copy()

        for i in range(len(operations)):
            operations[i] = operations[i].lower()
        operations.append("help")
        return operations

    @staticmethod
    def valid_file_extension(file: str) -> bool:
        file_extension = file.split(".")[-1]
        return f".{file_extension}" in VALID_EXTENSIONS
