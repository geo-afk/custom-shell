"""
This module provides a command-line interface for executing various file and system operations\n
based on the user's platform (Windows, Linux, or macOS). It supports commands for clearing the\n
screen, displaying help information, and performing file operations like creation and deletion.\n
The main function continuously prompts for user input and processes commands until the user
chooses to exit.
"""

from sys import platform
import logging
import os

from validator.static.exceptions import CustomBaseException
from validator.static.constant_types import ConsoleColors
from validator.static.constant_types import Platform
from Compute import ComputeOperations
from help_loader import LoadHelp
from input_parser import InputParser





logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Adjust as needed

# Console handler
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter("%(lineno)d - %(module)s - %(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)


def get_platform() -> Platform:
    """
    Gets the Operating System that the program is running on and check's
    then checks if O.S is Windows, Linux of Mac else raise OSError
    """

    if platform.startswith("win"):
        return Platform.WINDOWS
    if platform.startswith("linux"):
        return Platform.LINUX
    if platform.startswith("darwin"):
        return Platform.MAC

    raise OSError("Unsupported operating system")


def clear_screen():
    """
    The function `clear_screen()`\n
    clears the terminal screen based on the platform being used.
    """
    if get_platform() is Platform.WINDOWS:
        os.system("cls")
    else:
        os.system("clear")


def handle_help(parsed_input: str):
    """
    This function is used to handle the help command
    when the user request any help information
    whether it is general help
    or specific help
    for a command.
    :param parsed_input: List of parsed words from user input.
    """
    load_help = LoadHelp()
    help_data = ""


    if len(parsed_input) > 1:
        help_data = load_help.get_help_info(parsed_input[1])
    else:
        help_data = load_help.get_help_info()

    print(f"{ConsoleColors.get('CYAN')}{help_data}{ConsoleColors.get('RESET')}")


def handle_file_permissions(operating_system: Platform, parsed_input: list[str]):
    ...


def main():
    """
    Main Function where program starts
    gets the user input and does the computation if the user input is valid
    else prints out a clear Exception message telling the user why their
    input invalid and then starts back from scratch.
    """
    # main
    while True:
        os_platform = get_platform()

        print("\nEnter a command or ('e' to exit, 'c' to clear, 'help' for assistance):")
        command = input("custom_shell> ").strip()

        # Break out of program if the user enters e
        if command.lower() == "e":
            break

        # runs the clear screen command if user enters 'c'
        if command.lower() == "c":
            clear_screen()
            continue

        if command.lower().startswith("open"):
            ComputeOperations.open_file_or_folder(os_platform, command)
            clear_screen()
            continue


        try:
            # calling the `get_platform()` function to determine the operating
            # system platform the program is running on
            # pass in the input by the user for it to be parsed into a list of individual text
            # the call retrieved_parsed_input which validates the parsed list
            # if valid return list else raise and exception


            parsed_input = InputParser(command)
            parsed_input = parsed_input.retrieved_parsed_input()


            # If the user input is valid then check if the request\n
            # is of type help: 'if help is requested then check if\n
            # it is general help or a specific help'\n
            # if the input is not of help then call the compute class\n
            # to perform various operations like [create, delete, etc]

            if parsed_input[0] == "help":
                handle_help(parsed_input)
            else:
                compute = ComputeOperations(parsed_input, os_platform)
                compute.execute_operation()

        except CustomBaseException as e:
            # clear the screen and print the exception in #red if and error is risen
            clear_screen()
            print(f"{ConsoleColors.get('RED')}{e}{ConsoleColors.get('RESET')}")
            continue

        except Exception as e:
            # clear_screen()
            logger.error(e)
            continue



if __name__ == "__main__":
    main()
