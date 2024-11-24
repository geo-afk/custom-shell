from typing import List
import os

from validator.validator import Validator
from validator.static.exceptions import DirectoryManagementError

class DirectoryManagementValidator(Validator):

    def __init__(self, command: List[str]):
        super().__init__()
        self.command = command


    def validate(self):
        if len(self.command) == 1 and self.command[0] != "pwd":
            raise DirectoryManagementError(f"Invalid Command: '{self.command}' No path was given along with command")

        elif self.command[0] == "pwd" and len(self.command) > 1:
            raise DirectoryManagementError(f"Invalid Command: '{self.command[0]}'does take any params: {self.command[1:]}")

        elif self.command[0] == "pwd" and len(self.command) == 1:
            return True

        return self.validate_dir()

    
    def validate_dir(self):
        """
        Validates the directory command based on its requirements.
        """
        command = self.command[0]
        path_exists = self.path_exists()

        valid_conditions = {
            "change": path_exists,
            "remove": path_exists,
            "make": not path_exists,
        }


        if valid_conditions.get(command, False):
            return True

        raise DirectoryManagementError(f"Invalid Command: '{command}' for path existence is: {path_exists}")

    def path_exists(self):
        return os.path.exists(self.command[1])

