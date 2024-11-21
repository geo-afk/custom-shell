from enum import StrEnum
from typing import Dict, List


class FileOperation(StrEnum):
    """
        A string enum class used to store all the operations/ commands available to
        use in file operations.
    """
    CREATE = "create"
    DELETE = "delete"
    RENAME = "rename"


class FilePermission(StrEnum):
    """
        A string enum class used to store the permission commands and a list command to
        view files in directory.
    """
    MODIFY = "modify"
    LIST = "list"


class Platform(StrEnum):
    """
        A string enum class that stores the various platforms/ Operating Systems
        that the program supports.
    """
    WINDOWS = "win"
    LINUX = "linux"
    MAC = "darwin"



#A dictionary that maps each file operation to its corresponding commands
# for different platforms. Each key represents a FileOperation, and its value
# is a nested dictionary where keys are Platforms and values are lists of
# command-line arguments.
FILE_OPERATIONS: Dict[FileOperation, Dict[Platform, List[str]]] = {
    FileOperation.CREATE: {
        Platform.WINDOWS: ["cmd", "/c", "type", "nul", ">"],  # Command for creating a file on Windows
        Platform.LINUX: ["touch"],  # Command for creating a file on Linux
        Platform.MAC: ["touch"],  # Command for creating a file on macOS
    },
    FileOperation.DELETE: {
        Platform.WINDOWS: ["cmd", "/c", "del"],  # Command for deleting a file on Windows
        Platform.LINUX: ["rm"],  # Command for deleting a file on Linux
        Platform.MAC: ["rm"],  # Command for deleting a file on macOS
    },
    FileOperation.RENAME: {
        Platform.WINDOWS: ["cmd", "/c", "ren"],  # Command for renaming a file on Windows
        Platform.LINUX: ["mv"],  # Command for renaming a file on Linux
        Platform.MAC: ["mv"],  # Command for renaming a file on macOS
    },
}

# File Permissions for windows :
# example: icacls "C:\path\to\file.txt" /grant username:(R,W)
# F: Full control
# M: Modify
# RX: Read & execute
# R: Read-only
# W: Write-only
# Options using:
# /grant: Grants permissions to a user.
# /deny: Denies permissions for a user.
# /remove: Removes all permissions for a user.
# username:(R,W)



# File Permission for linux:
# example: chmod u=rwx,o=r <filename>
# r: Read (4)
# w: Write (2)
# x: Execute (1)
# Owner
# Group
# Others

# if not sure who are the users on a system can use [command to check users]

# mac uses the same commands as linus

FILE_PERMISSIONS: Dict[FilePermission, Dict[Platform, List[str]]] ={

    FilePermission.MODIFY: {
        Platform.WINDOWS: ["cmd", "/c","icacls", "path", "options", "username_permission"],
        Platform.MAC: ["chmod", "permission", "resource"],
        Platform.LINUX: ["chmod", "permission", "resource"]

    },
    FilePermission.LIST:{
        Platform.WINDOWS: ["cmd", "/c", "dir"],
        Platform.MAC: ["ls", "-l",],
        Platform.LINUX: ["ls", "-l",],
    }
}


# A dictionary to store different ASCII color codes for console output formatting.
ConsoleColors = {
    "RESET": "\033[0m",  # Resets color to default
    "RED": "\033[1;31m",  # Red color for text
    "BLUE": "\033[1;34m",  # Blue color for text
    "MAGENTA": "\033[1;35m",  # Magenta color for text
    "CYAN": "\033[1;36m",  # Cyan color for text
}


# A list that contains the valid file extensions that the program supports.
VALID_EXTENSIONS = [".txt", ".pdf", ".docx"]

# A list of valid pipe symbols that may be used in command-line operations.
PIPES: list[str] = ["<", ">", "|"]
