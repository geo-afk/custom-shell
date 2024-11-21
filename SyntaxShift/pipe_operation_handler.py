from typing import List


class PipeCommandHandler:

    def __init__(self, command):
        self.command = command

    def split_piped_commands(self) -> tuple[None | List[str], None | List[str]]:
        for i, arg in enumerate(self.command):
            if arg == "|":
                return self.command[:i], self.command[i + 1 :]
        return None, None