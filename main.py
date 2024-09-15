from typing import Dict, List
import os
import sys
import subprocess
from enum import Enum


class FileOperation(Enum):
    CREATE = "create"
    DELETE = "delete"
    RENAME = "rename"


class Platform(Enum):
    WINDOWS = "win"
    LINUX = "linux"
    MAC = "darwin"


FILE_OPERATIONS: Dict[FileOperation, Dict[Platform, List[str]]] = {
    FileOperation.CREATE: {
        Platform.WINDOWS: ["cmd", "/c", "type", "nul", ">"],
        Platform.LINUX: ["touch"],
        Platform.MAC: ["touch"]
    },
    FileOperation.DELETE: {
        Platform.WINDOWS: ["del"],
        Platform.LINUX: ["rm"],
        Platform.MAC: ["rm"]
    },
    FileOperation.RENAME: {
        Platform.WINDOWS: ["ren"],
        Platform.LINUX: ["mv"],
        Platform.MAC: ["mv"]
    }
}

VALID_EXTENSIONS = ['.txt', '.pdf', '.docx']


def get_platform() -> Platform:
    if sys.platform.startswith("win"):
        return Platform.WINDOWS
    elif sys.platform.startswith("linux"):
        return Platform.LINUX
    elif sys.platform.startswith("darwin"):
        return Platform.MAC
    else:
        raise OSError("Unsupported operating system")


def validate_file_extension(filename: str) -> bool:
    _, ext = os.path.splitext(filename)
    return ext.lower() in VALID_EXTENSIONS


def execute_command(command: List[str]) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(command, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Command output: {e.output}")
        return e


def process_file_operation(operation: FileOperation, filename: str, platform: Platform):
    if not validate_file_extension(filename):
        print(f"Error: Invalid file extension. Supported extensions are: {
              ', '.join(VALID_EXTENSIONS)}")
        return

    command = FILE_OPERATIONS[operation][platform]

    if operation == FileOperation.CREATE:
        if platform == Platform.WINDOWS:
            command = command + [filename]
        else:
            command = command + [filename]
    elif operation == FileOperation.DELETE:
        command = command + [filename]
    elif operation == FileOperation.RENAME:
        new_filename = input("Enter new filename: ")
        if not validate_file_extension(new_filename):
            print(f"Error: Invalid file extension for new filename. Supported extensions are: {
                  ', '.join(VALID_EXTENSIONS)}")
            return
        command = command + [filename, new_filename]

    result = execute_command(command)

    if result.returncode == 0:
        print(f"Operation successful: {operation.value} {filename}")
    else:
        print(f"Operation failed: {operation.value} {filename}")


def main():
    platform = get_platform()

    while True:
        user_input = input(
            "Enter command (create/delete/rename filename) or 'exit' to quit: ")
        if user_input.lower() == 'exit':
            break

        try:
            operation_str, filename = user_input.split(maxsplit=1)
            operation = FileOperation(operation_str.lower())
        except ValueError:
            print("Invalid input. Please use format: operation filename")
            continue
        except KeyError:
            print(f"Invalid operation. Supported operations are: {
                  ', '.join([op.value for op in FileOperation])}")
            continue

        process_file_operation(operation, filename, platform)


if __name__ == "__main__":
    main()
