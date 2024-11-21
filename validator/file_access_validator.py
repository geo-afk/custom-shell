
import os

from validator.static.exceptions import FileAccessError, InvalidCommand
from validator.validator import Validator

class FileAccessValidator(Validator):

    """
    Validates file access commands for correct syntax, file existence, and valid permissions.

    Attributes:
        access (list[str]): The file access command and associated parameters.
    Command:
         action = 'add', 'remove'
         permission = 'r', 'w', 'x'
        modify filePath action permission
    """

    VALID_ACTIONS = {'add', 'remove'}
    VALID_PERMISSIONS = {'r', 'w', 'x'}
    # modify ./file.txt add r w x
    def __init__(self, file_access):
        """
        Initialize the FileAccessValidator with a file access command.

        Args:
            file_access (list[str]): The file access command and associated parameters.
        """
        super().__init__()
        self.access: list[str] = file_access


    def validate(self):

        if not self.access or len(self.access) < 2:
            raise FileAccessError("Invalid command, command not of valid length...")

        if self.access[0] == "list":
            return self.validate_list()

        return self.validate_modify()


    def validate_list(self):

        folder_file_path = self.access[1]
        if not os.path.exists(folder_file_path):
            raise FileAccessError(f"Specified path does not exists, {folder_file_path}")

        return True

    def validate_modify(self):
        """
        Validate the file access command for correctness.

        Returns:
            bool: True if validation passes, otherwise raises an exception.

        Raises:
            InvalidCommand: If the command is of invalid length.
            FileAccessError: If the specified path does not exist.
        """

        if len(self.access) < 4:
            raise InvalidCommand(f"Invalid command, {self.access},length: {len(self.access)} (expected at least 4)")
        folder_file_path = self.access[1]
        if not os.path.exists(folder_file_path):
            raise FileAccessError(f"Specified path does not exists, {folder_file_path}")

        if not self.validate_action():
            raise InvalidCommand(f"Invalid action '{self.access[2]}'. Expected 'add' or 'remove'. , type help to see valid commands")

        if not self.validate_permission():
            invalid = self.find_invalid_permission()
            raise FileAccessError(f"Invalid permissions '{invalid}'. for file access, type help to see valid commands")

        return True

    def validate_action(self) -> bool:
        """
        Validate the action specified in the command.

        Returns:
            bool: True if the action is valid, False otherwise.
        """

        action: str = self.access[2]
        return action in FileAccessValidator.VALID_ACTIONS

    def validate_permission(self) -> bool:
        """
        Validate the permissions specified in the command.

        Returns:
            bool: True if the permissions are valid, False otherwise.
        """
        permission = self.access[3:]

        # Check basic constraints: length must be between 1 and 3, must contain 'f' if length is 1
        if not (1 <= len(permission) <= 3) or (len(permission) == 1 and permission[0] != 'f'):
            return False

        # Check that all characters are valid permissions ('r', 'w', 'x') and no 'f' is present
        if not all(p in FileAccessValidator.VALID_PERMISSIONS for p in permission):
            return False

        return True

    def find_invalid_permission(self):
        permission = self.access[3:]
        valid = FileAccessValidator.VALID_PERMISSIONS
        invalid: list[str] = [p for p in permission if p not in valid]

        return invalid