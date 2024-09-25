from static.exceptions import CommonException, FileOperationError, InvalidCommand
from static.constant_types import Platform
from static.constant_types import ConsoleColors
from input_parser import InputParserAndValidator
from help_parser import HelpFile
from Compute import ComputeOperations
from sys import platform
import os


def get_platform() -> Platform:
    if platform.startswith("win"):
        return Platform.WINDOWS
    elif platform.startswith("linux"):
        return Platform.LINUX
    elif platform.startswith("darwin"):
        return Platform.MAC
    else:
        raise OSError("Unsupported operating system")


def main():
    while True:
        print("\nEnter a command ('e' to exit, 'c' to clear, 'help' for assistance):")
        command = input(">> ").strip()

        if command.lower() == "e":
            break

        if command.lower() == "c":
            os.system("cls")
            continue

        try:
            platform = get_platform()
            parsed_input = InputParserAndValidator(command)
            parsed_input = parsed_input.retrieved_parsed_input()

            if parsed_input[0] == "help":
                if len(parsed_input) > 1:
                    help_details = HelpFile.get_general_help(parsed_input[1])
                    print(
                        f"{ConsoleColors.CYAN.value}{help_details}{ConsoleColors.RESET.value}"
                    )
                else:
                    for command, details in HelpFile.get_basic_help():
                        print(
                            f"{ConsoleColors.CYAN.value}{command}: {details}{ConsoleColors.RESET.value}"
                        )
            else:
                compute = ComputeOperations(parsed_input, platform)
                compute.execute_operation()

        except (CommonException, InvalidCommand, FileOperationError) as e:
            os.system("cls")
            print(f"{ConsoleColors.RED.value}{e}{ConsoleColors.RESET.value}")
            continue


if __name__ == "__main__":
    main()
