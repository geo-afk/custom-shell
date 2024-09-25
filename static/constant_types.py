from enum import Enum
from typing import Dict, List


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
        Platform.MAC: ["touch"],
    },
    FileOperation.DELETE: {
        Platform.WINDOWS: ["cmd", "/c", "del"],
        Platform.LINUX: ["rm"],
        Platform.MAC: ["rm"],
    },
    FileOperation.RENAME: {
        Platform.WINDOWS: ["cmd", "/c", "ren"],
        Platform.LINUX: ["mv"],
        Platform.MAC: ["mv"],
    },
}


class ConsoleColors(Enum):
    RESET = "\033[0m"
    RED = "\033[1;31m"
    BLUE = "\033[1;34m"
    MAGENTA = "\033[1;35m"
    CYAN = "\033[1;36m"


VALID_EXTENSIONS = [".txt", ".pdf", ".docx"]
PIPES: list[str] = ["<", ">", "|"]
