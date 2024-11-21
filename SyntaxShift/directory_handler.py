from validator.static.constant_types import DIRECTORY_OPERATIONS, DirectoryOperation
from validator.static.exceptions import DirectoryManagementError


class DirectoryManagementHandler:

    def __init__(self, operation, operation_system):
        self.operation = operation
        self.operating_system = operation_system


    def make_directory_command(self):

        operation = DirectoryOperation(self.operation[0])
        command = DIRECTORY_OPERATIONS[operation][self.operating_system]

        if operation == DirectoryOperation.CURRENT:
            return command
        return command + [self.operation[1]]
