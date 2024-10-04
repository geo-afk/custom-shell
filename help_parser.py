from dataclasses import  dataclass
from typing import Dict
import json

@dataclass
class General:
    """
        This class is used to store the general - specific help
        for the help command, for each operation it stores details
        to which can be retrieved one by one, using the
        help_command function.
    """
    create: str
    delete: str
    rename: str

    def help_command(self, command: str) -> str:
        """
            This function is used to check if the command for which
            the help/details, is requested for by the user is a defined
            variable/attribute of the class if it is then it returns it
            if it is not it returns and empty string

            :param command: specific command for which the help operation is requesting.
            :return: the details of a specific command
        """
        return getattr(self, command, "")

@dataclass
class Info:

    """
        This class is used to store the information for all the supported commands.
        This class is used to print all the available command details
        and give a small overview of all the commands,
        the dunder '__str__' method is used for printing details of all the
        supported commands.
    """
    create: str
    delete: str
    rename: str



    def __str__(self) -> str:
        return "\n ".join([self.create, self.delete, self.rename])





@dataclass
class Help:
    """
        This class is used to store all the types of help
        operations that is supported
        1. The general/specific help, ex: 'help delete'
        2. The information help which prints out all the
        supported command and a small detail of each

        This class used the dunder '__post_init__' method
        provided by data class to
        initialize the variables of the class shortly
        after the constructor for 'Help' class
        is called. This is done as the help class doesn't
        directly call the constructor
        of the composed classes.
    """
    general: General
    info: Info

    # noinspection PyArgumentList
    def __post_init__(self):
        # noinspection PyArgumentList
        self.general = General(**self.general)
        self.info = Info(**self.info)



class LoadHelp:
    """
        This class is used to load the details from the json file which contain all the
        details of the supported operation,
        and when the 'get_help' function is called it calls the 'load_help_data' function
        which gets the details from the json file then
        it serializes that information into the 'Help' class and returns it
        unless and error occurs then the raises a 'ValueError' in which is graciously
        caught then a formatted output is printed to the console in #FF0000|RED.
    """
    def __init__(self) -> None:
        self._help_data: Help | None = None

    @staticmethod
    def load_help_data() -> Dict:
        with open("./static/help.json", "r") as f:
            return json.load(f)

    def get_help(self) -> Help | None:
        if self._help_data is None:
            data = self.load_help_data()
            try:
                self._help_data = Help(**data)
            except ValueError as e:
                print(f"\033[91m{e}\033[0m")
                return None
        return self._help_data