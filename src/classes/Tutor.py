

# Each experience constant stores the regex pattern that extracts itself from a raw string
STUDENT_OR_PART_TIME=r"student|part-time|part time|part|private"
GRADUATE_OR_FULL_TIME=r"graduate|full-time|full time|full"
EX_CURRENT_MOE=r"moe|nie|teacher"

# Establishing the hierarchy for tutor experience
ALL_TUTOR_EXPERIENCES_RANKED = [STUDENT_OR_PART_TIME,GRADUATE_OR_FULL_TIME,EX_CURRENT_MOE]

# Subjects constants - associated with a regex pattern
ENGLISH=r"english"
CHINESE=r"chinese"
MATH=r"math"
SCIENCE=r"science"
PHYSICS=r"physics"
CHEMISTRY=r"chemistry|chem"
BIOLOGY=r"biology|bio"
COMPUTING=r"computing|computer science"
LITERATURE=r"literature|lit"
GENERAL_PAPER=r"general paper|gp"
POA=r"poa|principle of accounts"
MALAY=r"malay"
TAMIL=r"tamil"
ECONOMICS=r"econs|economics"
ACCOUNTING=r"accounting"
HISTORY=r"history"

# Add all subjects to a constant list. 
# I'm using this as convenience to extract subjects from a raw message
ALL_SUBJECTS=[ENGLISH,CHINESE,MATH,SCIENCE,PHYSICS,
              CHEMISTRY,BIOLOGY,COMPUTING,LITERATURE,GENERAL_PAPER,
              POA,MALAY,TAMIL,ECONOMICS,ACCOUNTING,HISTORY]

# Subject levels
NURSERY_KINDERGARTEN_LEVEL = r"nursery|kindergarten|k[1-2]"
PRIMARY_LEVEL = r"primary [1-6]|p[1-6]|pri|psle"
SECONDARY_LEVEL = r"secondary|sec [1-5]|sec|o-level|o level"
POLYTECHNIC_LEVEL = r"poly|polytechnic"
JUNIOR_COLLEGE_LEVEL = r"jc|junior college|jc[1-2]|a-level|a level|h[1-3]"
IB_LEVEL=r"ib"
IGCSE_LEVEL=r"igcse"
UNIVERSITY_LEVEL = r"university"
## For detail extraction
ALL_SUBJECT_LEVELS = [NURSERY_KINDERGARTEN_LEVEL,PRIMARY_LEVEL,SECONDARY_LEVEL,
                      POLYTECHNIC_LEVEL,JUNIOR_COLLEGE_LEVEL,
                      IB_LEVEL,IGCSE_LEVEL,UNIVERSITY_LEVEL]

# Address for online tuition
ONLINE_TUITION = "online"

# Gender constants
MALE='male'
FEMALE='female'
NON_BINARY='non-binary'
## For detail extraction
ALL_GENDERS=[FEMALE,NON_BINARY,MALE]

# Commuting constants for Google Directions API parameters TODO: modify get_directions() method
PUBLIC_TRANSPORT="transit" # mode=Tutor.PUBLIC_TRANSPORT,transit_mode=["bus","rail"]
DRIVING="driving" # mode=Tutor.DRIVING

class Tutor():
    def __init__(
            self, 
            name: str, 
            telegram_handle: str, 

            subjects: set[str], 
            subject_levels: set[str],
            experience: set[str], 

            address: str, 
            gender:set[str],
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

        subjects={MATH,SCIENCE,PHYSICS,CHEMISTRY,COMPUTING},
        experience={GRADUATE_OR_FULL_TIME},
        subject_levels={SECONDARY_LEVEL,POLYTECHNIC_LEVEL},

        address="40B Margaret Drive",
        gender={MALE},
        commute_method=PUBLIC_TRANSPORT,
        max_commute_time=40,
    )
MUM = Tutor(
    name="Mum 🌸",
    telegram_handle="@Nekotokuma",

    subjects={ENGLISH,SCIENCE},
    experience={EX_CURRENT_MOE},
    subject_levels={PRIMARY_LEVEL,SECONDARY_LEVEL},

    address="40B Margaret Drive",
    gender={FEMALE},
    commute_method=PUBLIC_TRANSPORT,
    max_commute_time=40,
)

# Make an importable list
TUTOR_LIST:list[Tutor] = [
    RIAN,
    MUM,
    Tutor(
        name="Rachel",
        telegram_handle="@rachellor",

        subjects={MATH,ENGLISH,LITERATURE,CHEMISTRY,GENERAL_PAPER},
        experience={GRADUATE_OR_FULL_TIME},
        subject_levels={SECONDARY_LEVEL,POLYTECHNIC_LEVEL},

        address="Sembawang MRT",
        gender={FEMALE},
        commute_method=PUBLIC_TRANSPORT,
        max_commute_time=40,
    ),
    Tutor(
        name="Delia",
        telegram_handle="@ddxliaa",

        subjects={MATH},
        experience={GRADUATE_OR_FULL_TIME},
        subject_levels={JUNIOR_COLLEGE_LEVEL},

        address=ONLINE_TUITION,
        gender={FEMALE},
        commute_method=None,
        max_commute_time=None,
    )
]