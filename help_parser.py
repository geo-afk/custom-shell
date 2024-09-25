from typing import Dict, List, Optional, Any
from static.exceptions import CommonException

import json


type FILEDATA = Dict[str, str] | Any


class HelpFile:
    general_help: Optional[FILEDATA] = None
    basic_help: Optional[FILEDATA] = None

    @staticmethod
    def load_help_data() -> FILEDATA:
        """Load help data from the JSON file."""
        with open("./static/help.json", "r") as f:
            return json.load(f)

    @classmethod
    def validate_help_info(
        cls, data: FILEDATA, help_type: str
    ) -> Optional[Dict[str, str]]:
        help_data = data.get(help_type)
        return help_data if isinstance(help_data, dict) else None

    @classmethod
    def load_help_details(cls, help_type: str) -> None:
        """Generalized method to load help data."""
        data = cls.load_help_data()
        if help_type == "general":
            cls.general_help = cls.validate_help_info(data, "general")
        elif help_type == "info":
            cls.basic_help = cls.validate_help_info(data, "info")

    def list_of_general_help(self) -> Optional[List[str]]:
        return list(HelpFile.general_help.keys()) if HelpFile.general_help else None

    @classmethod
    def get_general_help(cls, command_name: str) -> str:
        cls.load_help_details("general")

        help_file = cls.general_help.get(command_name) if cls.general_help else None
        if help_file:
            return help_file

        raise CommonException(f"Command is not supported.. [{command_name} not found] ")

    @classmethod
    def get_basic_help(cls) -> dict[str, str] | Any:
        cls.load_help_details("info")
        print("\n")

        if cls.basic_help is not None:
            return cls.basic_help.items()
        return None
