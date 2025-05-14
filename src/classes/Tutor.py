from typing import List


class Tutor():
    def __init__(self, name: str, telegram_handle: str, subjects: List[str], experience: List[str], address: str, gender:str):
        self.name = name
        self.telegram_handle = telegram_handle
        self.subjects = subjects
        self.experience = experience
        self.address = address
        self.gender = gender

# Instantianting my predefined tutor filters
RIAN = Tutor(
        name="Rian 🪴",
        telegram_handle="@rianhuii",
        subjects=[
            "math",
            "science",
            "physics",
            "chemistry",
            "computing"
        ],
        experience=[
            "student",
            "part",
            "full",
            "private",
        ],
        address="40B Margaret Drive",
        gender="male",
    )
MUM = Tutor(
    name="Mum 🌸",
    telegram_handle="@Nekotokuma",
    subjects=[
        "english",
        "science",
    ],
    experience=[
        "full",
        "moe",
        "private",
        "above",
    ],
    address="40B Margaret Drive",
    gender="female",
)

# Make an importable list
TUTOR_LIST:List[Tutor] = [RIAN,MUM]