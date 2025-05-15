
# Establishing the hierarchy for tutor experience
TUTOR_EXPERIENCE_HIERARCHY = {
    "Student/Part-time":1,
    "Graduate/Full-time":2,
    "Ex/Current MOE":3
} 

class Tutor():
    def __init__(
            self, 
            name: str, 
            telegram_handle: str, 
            subjects: list[str], 
            subject_levels: list[str],
            experience: int, 
            address: str, 
            gender:str,
            commute_method:list[str],
            max_commute_time:int):
        self.name = name
        self.telegram_handle = telegram_handle
        self.subjects = subjects
        self.subject_levels = subject_levels
        self.experience = experience
        self.address = address
        self.gender = gender
        self.commute_method = commute_method
        self.max_commute_time = max_commute_time

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
        subject_levels=[
            r" sec | secondary ",
            r" poly | polytechnic ",
        ],
        address="40B Margaret Drive",
        gender="male",
        commute_method=["bus","rail"],
        max_commute_time=30,
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
    subject_levels=[
            r" sec | secondary ",
            r" pri | primary | p[1-6] ",
    ],
    address="40B Margaret Drive",
    gender="female",
    commute_method=["bus","rail"],
    max_commute_time=30,
)

# Make an importable list
TUTOR_LIST:list[Tutor] = [
    RIAN,
    MUM,
    Tutor(
        name="Rachel",
        telegram_handle="@rachellor",
        subjects=[
            "math",
            "english",
            "literature",
            "chemistry",
            "general paper"
        ],
        experience=[
            "full",
            "private",
            "above",
        ],
        subject_levels=[
                r" sec | secondary ",
                r" poly | polytechnic ",
        ],
        address="Sembawang MRT",
        gender="female",
        commute_method=["bus","rail"],
        max_commute_time=30,
    )
]