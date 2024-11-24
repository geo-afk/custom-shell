from validator.validator import Validator

class HelpValidator(Validator):

    def __init__(self, parsed_inputs):
        super().__init__()
        self.parsed_inputs = parsed_inputs


    def valid_help_input(self):
        """
            if the user request to use the help operation, this function is called to validate
            the user input for the help command, it checks id the user is requesting
            specific help for a supported command or the general help where list all
            supported commands.
            :return: True or False.
        """
        valid_help = set(self.get_valid_operations()) - {"help"}
        if len(self.parsed_inputs) == 1:
            return True

        return self.parsed_inputs[1] in valid_help