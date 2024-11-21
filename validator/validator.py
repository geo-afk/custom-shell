from typing import List

from validator.static.constant_types import FileOperation, FilePermission, DirectoryOperation


class Validator:


    def __init__(self):
        self.VALID_OPERATIONS: List[str] = self.get_valid_operations()

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
        operations = [
            operation.value
            for group in (FileOperation, FilePermission, DirectoryOperation)
            for operation in group
        ]
        operations.append("help")
        return operations


