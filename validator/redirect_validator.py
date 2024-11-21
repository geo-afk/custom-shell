import os
from typing import List

from validator.validator import Validator
from validator.static.constant_types import  VALID_EXTENSIONS
from validator.static.exceptions import InvalidCommand


class RedirectValidator(Validator):
    """
    Validates commands with input/output redirection.

    Attributes:
        command (List[str]): The user command to validate.
    """

    REDIRECT = ['<', '>']

    def __init__(self, command: List[str]):
        """
        Initialize the RedirectValidator.

        Args:
            command (List[str]): The user command to validate.
        """
        super().__init__()
        self.command: List[str] = command

    def validate(self) -> bool:
        """
        Validate the entire command for correct redirection.

        Returns:
            bool: True if the command is valid, raises an exception otherwise.

        Raises:
            InvalidCommand: If an invalid redirection is detected.
        """

        if not any(symbol in self.command for symbol in self.REDIRECT):
            raise InvalidCommand("No redirection symbol ('<' or '>') found in the command.")

        if '>' in self.command:
            return self.into_redirect()

        if '<' in self.command:
            return self.from_redirect()

        return True

    def into_redirect(self) -> bool:
        """
        Validate the output redirection (`>`) in the command.

        Returns:
            bool: True if the output redirection is valid.

        Raises:
            InvalidCommand: If the output file is invalid.
        """
        try:
            index = self.command.index(self.REDIRECT[1]) + 1
            return self.validate_file_extention(index)
        except (ValueError, IndexError) as e:
            raise InvalidCommand(
                "Output redirection symbol ('>') is missing a valid file."
            ) from e

    def from_redirect(self) -> bool:
        """
        Validate the input redirection (`<`) in the command.

        Returns:
            bool: True if the input redirection is valid.

        Raises:
            InvalidCommand: If the input file is invalid.
        """
        commands = set(self.get_valid_operations()) - {"help", "pwd"}
        index = self.command.index(self.REDIRECT[0]) + 1
        file_exists = self.check_file_exists(index)


        if self.command[0] not in commands:
            raise InvalidCommand(f"Into Redirect is invalid, command not supported {self.command}")

        if not file_exists:
            raise InvalidCommand("Invalid redirect from file command, file does not exist.")
        try:
            return self.validate_file_extention(index)
        except (ValueError, IndexError) as e:
            raise InvalidCommand(
                "Input redirection symbol ('<') is missing a valid file."
            ) from e


    def validate_file_extention(self, index):


        file: str = self.command[index]

        if '.' not in file or f".{file.split('.')[-1]}" not in VALID_EXTENSIONS:
            raise InvalidCommand(f"Invalid file extension for input redirection: {file}")

        return True

    def check_file_exists(self, index):
        file = self.command[index]
        return os.path.exists(file)

