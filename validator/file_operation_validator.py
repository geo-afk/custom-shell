from validator.validator import Validator
from validator.static.constant_types import VALID_EXTENSIONS
from validator.static.exceptions import FileOperationError

class FileOperationValidator(Validator):

    def __init__(self, args):
        super().__init__()
        if len(args) != 1:
            raise FileOperationError(f"Invalid file operation is invalid length, for file: {args}")
        self.args: list[str] = args


    def is_operation_valid(self) -> bool:
        """
            Validates the operation and its arguments.
            This function checks whether both the operation and the provided arguments are valid.
            For example, if the user wants to create a file, the function checks if the operation
            is 'create' and the arguments include a valid file extension (e.g., 'filename.txt').
            :return: True if both the operation and its arguments are valid.
        """

        if self.valid_file_extension(self.args[0]):
            return True

        raise FileOperationError(f"Invalid or missing file extention.. {self.args[0]}")


    @staticmethod
    def valid_file_extension(file: str) -> bool:
        """
            function is used check if the inputted file from the user
            has a supported file extension
        """
        file_extension = file.split(".")[-1]
        return f".{file_extension}" in VALID_EXTENSIONS