from typing import List


class Tutor():
    def __init__(self, name: str, subjects: List[str], experience: List[str], address: str):
        self.name = name
        self.subjects = subjects
        self.experience = experience
        self.address = address

# Instantianting my predefined tutor filters
RIAN = Tutor(
        name="Rian 🪴",
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
        ],
        address="40B Margaret Drive"
    )
MUM = Tutor(
    name="Mum 🌸",
    subjects=[
        "english",
        
    ],
    experience=[
        "full",
        "moe",
    ],
    address="40B Margaret Drive"
)

# Make an importable list
TUTOR_LIST:List[Tutor] = [RIAN,MUM]