
# Establishing the hierarchy for tutor experience
STUDENT_OR_PART_TIME=1
GRADUATE_OR_FULL_TIME=2
EX_CURRENT_MOE=3

# Subjects constants - can be associated with a regex pattern perhaps?
ENGLISH="english"
CHINESE="chinese"
MATH="math"
SCIENCE="science"
PHYSICS="physics"
CHEMISTRY="chemistry"
BIOLOGY="biology"
COMPUTING="computing"
LITERATURE="literature"
GENERAL_PAPER="general paper"

# Subject levels
PRIMARY_LEVEL = r" pri | primary | p[1-6] "
SECONDARY_LEVEL = r" sec | secondary "
POLYTECHNIC_LEVEL = r" poly | polytechnic "
JUNIOR_COLLEGE_LEVEL = r" jc | junior college | jc[1-2]"

# Address for online tuition
ONLINE_TUITION = "online"

# Gender constants
MALE='male'
FEMALE='female'

# Commuting constants for Google Directions API parameters TODO: modify get_directions() method
PUBLIC_TRANSPORT="transit" # mode=Tutor.PUBLIC_TRANSPORT,transit_mode=["bus","rail"]
DRIVING="driving" # mode=Tutor.DRIVING

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
        self.address = address # None if tutor is online
        self.gender = gender
        self.commute_method = commute_method
        self.max_commute_time = max_commute_time # None if tutor is online

# Instantianting my predefined tutor filters
RIAN = Tutor(
        name="Rian 🪴",
        telegram_handle="@rianhuii",
        subjects=[MATH,SCIENCE,PHYSICS,CHEMISTRY,COMPUTING],
        experience=2,
        subject_levels=[SECONDARY_LEVEL,POLYTECHNIC_LEVEL],
        address="40B Margaret Drive",
        gender=MALE,
        commute_method=PUBLIC_TRANSPORT,
        max_commute_time=30,
    )
MUM = Tutor(
    name="Mum 🌸",
    telegram_handle="@Nekotokuma",
    subjects=[ENGLISH,SCIENCE],
    experience=3,
    subject_levels=[PRIMARY_LEVEL,SECONDARY_LEVEL],
    address="40B Margaret Drive",
    gender=FEMALE,
    commute_method=PUBLIC_TRANSPORT,
    max_commute_time=30,
)

# Make an importable list
TUTOR_LIST:list[Tutor] = [
    RIAN,
    MUM,
    Tutor(
        name="Rachel",
        telegram_handle="@rachellor",
        subjects=[MATH,ENGLISH,LITERATURE,CHEMISTRY,GENERAL_PAPER],
        experience=2,
        subject_levels=[SECONDARY_LEVEL,POLYTECHNIC_LEVEL],
        address="Sembawang MRT",
        gender=FEMALE,
        commute_method=PUBLIC_TRANSPORT,
        max_commute_time=30,
    ),
    Tutor(
        name="Delia",
        telegram_handle="@ddxliaa",
        subjects=[MATH],
        experience=2,
        subject_levels=[JUNIOR_COLLEGE_LEVEL],
        address=ONLINE_TUITION,
        gender=FEMALE,
        commute_method=None,
        max_commute_time=30,
    )
]