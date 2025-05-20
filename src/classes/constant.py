
# Defining my own constants class
# Contains a name and a regex pattern

class Constant():
    def __init__(
            self,
            name:str,
            regex_pattern:str):
        self.name = name
        self.regex_pattern = regex_pattern