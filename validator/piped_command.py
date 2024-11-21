from typing import List

from validator.validator import Validator

class PipedCommandValidator(Validator):
    """
    Validates piped commands to ensure operations on the right-hand side are valid.
    """

    VALID_PIPED_COMMANDS = {
        'list': 'modify',
        'create': 'list',
        'delete': 'list',
        'rename': 'list',
        'make': 'list',
        'remove': 'list',
        'change': 'list',
    }

    def __init__(self, command):
        """
        Initialize the validator with a command.

        Args:
            command (List[str]): The left-hand side command of the piped operation.
        """
        super().__init__()
        self.command: List[str] = command

    def get_piped_command(self):
        """
        Extracts and returns the portion of the command list following a pipe ("|").
        """
        if "|" in self.command:
            pipe_index = self.command.index("|")
            return self.command[pipe_index + 1:]
        return []

    def valid_piped_operations(self) -> bool:
        """
        Validates the right-hand side operations in a piped command.

        Returns:
            bool: True if the piped operations are valid, False otherwise.

        Raises:
            ValueError: If the piped operations list is empty.
        """

        piped_operations: list[str] = self.get_piped_command()
        if not piped_operations:
            raise ValueError("Piped operations cannot be empty.")

        valid_operations = set(self.get_valid_operations())
        valid_operations.discard("help")  # Exclude "help" from valid piped operations.


        if piped_operations[0] not in valid_operations:
            return False

        if self.command[0] == piped_operations[0]:
            return False # Prevent self-referential operations.


        required_command = PipedCommandValidator.VALID_PIPED_COMMANDS.get(self.command[0])
        if not required_command or required_command != piped_operations[0]:
            return False
        return True

