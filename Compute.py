"""
    This module is used to translate the commands of the user
    into command line argument and executing them depending on the user
    operating system.
    the program works by figuring out if the requested operations
    is a piped command or non-piped command
    and executing them accordingly,
    the program also check if operation requested is 'delete or rename'
    operation, if:
    delete then it checks if the file exists first before deleting any file,
    rename: it also checks if the file already exists before doing rename operation
"""

from time import sleep
from typing import List, Optional
import subprocess
import os

from SyntaxShift.redirect_handlier import RedirectHandler
from SyntaxShift.file_access_handler import FileAccessHandler
# from SyntaxShift.pipe_operation_handler import PipeCommandHandler
from SyntaxShift.file_operation_handler import FileOperationHandler
from SyntaxShift.directory_handler import DirectoryManagementHandler
from validator.static.constant_types import Platform, DirectoryOperation, FileOperation,FilePermission, ConsoleColors


class ComputeOperations:
    """
        This class handles executing the parsed commands passed,
        whether the command is a piped command normal command, it starts by,
        sectioning down the input into the various categories for supported commands,
        ex: create, delete, rename, e.t.c, after this step it then
        breaks down the command into pieces if the command is a piped command

    """
    def __init__(self, command_args: List[str], operating_system: Platform) -> None:
        self.command_args = command_args
        self.platform = operating_system


    @staticmethod
    def open_file_or_folder(operating_system: Platform, path_name: str):
        if os.path.exists(path_name):
            try:
                    if operating_system.WINDOWS:
                        os.startfile(path_name)
                    if operating_system.MAC:
                        subprocess.run(["open", path_name], check=True)
                    if operating_system.LINUX:
                        subprocess.run(["xdg-open", path_name], check=True)
            except subprocess.CalledProcessError as error:
                print(f"Error while opening resource...{error}")
        else:
            print("No resource is available at this path")




    def execute_operation(self) -> None:
        if "|" in self.command_args:
            pass

        # elif "<" in self.command_args:
        #     self.redirect_input()

        elif ">" in self.command_args:
            self.redirect_output()
        else:
            self.execute_single_command()


    def execute_single_command(self):
        command = self.command_args[0]
        operation = None
        if command in DirectoryOperation:
            if command == "change":
                # Change directory in the parent process
                os.chdir(self.command_args[1])
            directory_hadlier = DirectoryManagementHandler(self.command_args, self.platform)
            operation = directory_hadlier.make_directory_command()
            print(operation)

        elif command in FileOperation:
            file_operation = FileOperationHandler(self.command_args, self.platform)
            if command == "rename":
                new_filename = input("Enter new filename: ")
                operation = file_operation.check_file_operation(new_filename)
            else:
                operation = file_operation.check_file_operation()

        elif command in FilePermission:
            file_permission = FileAccessHandler(self.command_args, self.platform)
            operation = file_permission.check_file_access()


        completed = self.execute_command(operation)
        if command == "pwd" or command == "list":
            print(f"\n{ConsoleColors.get('MAGENTA')}{completed}{ConsoleColors.get('RESET')}")


# self.execute_piped_command(first_cmd, second_cmd)

    @staticmethod
    def execute_piped_command(first_command: List[str], second_command: List[str]) -> None:
        with subprocess.Popen(first_command, stdout=subprocess.PIPE) as first_process:
            with subprocess.Popen(second_command, stdin=first_process.stdout, stdout=subprocess.PIPE) as piped_process:
                if first_process.stdout:
                    first_process.stdout.close()
                output, _ = piped_process.communicate()
                print(output.decode("utf-8"))

    @staticmethod
    def execute_command(command: List[str]) -> str | None:
        try:
            result = subprocess.run(
                args=command,
                check=True,
                capture_output=True,
                text=True)

            return result.stdout

        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
            print(f"Command output: {e.stdout}")
            print(f"Command error output: {e.stderr}")
            return None


    def redirect_output(self):
        """
        Redirect command output to a file.

        Example:
            redirect_output(['ls'], 'output.txt')
        """

        redirect_commands = RedirectHandler(self.command_args, self.platform, ">")
        command: List[str] = redirect_commands.check_redirect_operation()

        fix_index = self.command_args.index(">")
        file_path = self.command_args[fix_index+1]

        with open(file_path, 'w') as f:
            result = subprocess.run(command,capture_output=True, text=True)

            if result and result.returncode == 0:
                f.write(result.stdout)
                print(result.stdout)
        sleep(5)

    def redirect_input(self):
        """
        Redirect input from a file to a command.
        Example:
            redirect_input(['cat'], 'input.txt')
        """

        redirect_commands = RedirectHandler(self.command_args, self.platform, "<")
        command = redirect_commands.check_redirect_operation()

        file_path = ""

        for i in range(len(self.command_args)):
            if self.command_args[i] == '<':
                file_path = self.command_args[i + 1]
                break

        with open(file_path, 'r') as f:
            subprocess.run(command + [f.read()], stdin=f, capture_output=True, text=True)

