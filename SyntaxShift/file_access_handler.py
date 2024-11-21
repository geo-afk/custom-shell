from os import getlogin

from validator.static.constant_types import FilePermission
from validator.static.constant_types import FILE_PERMISSIONS, Platform
from validator.static.exceptions import FileAccessError, InvalidCommand

class FileAccessHandler:

    """
    Handles file access operations for different platforms.

    Attributes:
        command (list[str]): The command specifying file operation and permissions.
        operating_system (Platform): The operating system platform.
    """

    UNIX_PLATFORMS = [Platform.LINUX, Platform.MAC]
    ADD = "add"
    REMOVE = "remove"
    GRANT = "/grant"
    REMOVE_PERMISSION = "/remove"
    UNIX_ADD = "u+"
    UNIX_REMOVE = "u-"

    def __init__(self, command: list[str], operating_system: Platform):
        if not command:
            raise ValueError("Command is null..!")
        self.command = command
        self.operating_system = operating_system


    def check_file_access(self):

        operation = FilePermission(self.command[0])

        if self.command[0] == "list":
            return FILE_PERMISSIONS[operation][self.operating_system]+ [self.command[1]]



        if not self.command or len(self.command) < 4:
            raise ValueError("Invalid command. Must contain operation, file, access type, and permissions.")
        access: list[str] = self.retrieve_access()


        if self.operating_system == Platform.WINDOWS:
            permission = self.retrieve_windows_permission()

            return FILE_PERMISSIONS[operation][self.operating_system]+ [self.command[1]] + access + permission

        elif self.operating_system in FileAccessHandler.UNIX_PLATFORMS:
            permission = self.retrieve_unix_permission(access)
            return FILE_PERMISSIONS[operation][self.operating_system] + permission + [self.command[1]]


        raise InvalidCommand(f"Invalid file access command, {self.command}")


    def retrieve_unix_permission(self, access: list[str]):

        permissions = ''.join(set(self.command[3:]))
        command = ''.join(access) + permissions

        return [command]



    def retrieve_windows_permission(self):
        current_user = getlogin()
        permissions = ','.join(permission.upper() for permission in set(self.command[3:]))
        return [f"{current_user}:({permissions})"]


    def retrieve_access(self):

        commands = {
            FileAccessHandler.ADD: {
                Platform.WINDOWS: [FileAccessHandler.GRANT],
                Platform.LINUX: [FileAccessHandler.UNIX_ADD],
                Platform.MAC: [FileAccessHandler.UNIX_ADD]
            },
            FileAccessHandler.REMOVE: {
                Platform.WINDOWS: [FileAccessHandler.REMOVE_PERMISSION],
                Platform.LINUX: [FileAccessHandler.UNIX_REMOVE],
                Platform.MAC: [FileAccessHandler.UNIX_REMOVE]
            }
        }

        try:
            return commands[self.command[2]][self.operating_system]
        except KeyError:
            raise FileAccessError(f"Invalid file access command '{self.command[2]}'. Valid options are 'add' or 'remove'.")




