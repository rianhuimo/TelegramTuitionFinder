from .constant import Constant

# Each experience constant stores the regex pattern that extracts itself from a raw string
STUDENT_OR_PART_TIME=Constant("Student/Part-Time",r"student|part-time|part time|part|private")
GRADUATE_OR_FULL_TIME=Constant("Graduate/Full-Time",r"graduate|full-time|full time|full")
EX_CURRENT_MOE=Constant("Ex/Current MOE/NIE",r"moe|nie")

# Establishing the hierarchy for tutor experience
ALL_TUTOR_EXPERIENCES_RANKED:list[Constant] = [STUDENT_OR_PART_TIME,GRADUATE_OR_FULL_TIME,EX_CURRENT_MOE]

# Subjects constants - associated with a regex pattern
ENGLISH=Constant("English",r"english")
CHINESE=Constant("Chinese",r"chinese")
MATH=Constant("Math",r"math")
SCIENCE=Constant("Science",r"science")
PHYSICS=Constant("Physics",r"physics")
CHEMISTRY=Constant("Chemistry",r"chemistry|chem")
BIOLOGY=Constant("Biology",r"biology|bio")
COMPUTING=Constant("Computing",r"computing|computer science")
LITERATURE=Constant("Literature",r"literature|lit")
GENERAL_PAPER=Constant("General Paper",r"general paper|gp")
POA=Constant("POA",r"poa|principle of accounts")
MALAY=Constant("Malay",r"malay")
TAMIL=Constant("Tamil",r"tamil")
ECONOMICS=Constant("Economics",r"econs|economics")
ACCOUNTING=Constant("Accounting",r"accounting")
HISTORY=Constant("History",r"history")
GEOGRAPHY=Constant("Geography",r"geography|geo")
MUSIC=Constant("Music",r"music|violin|piano")
ART=Constant("Art",r"art")

# Add all subjects to a constant list. 
# I'm using this as convenience to extract subjects from a raw message
ALL_SUBJECTS:list[Constant]=[ENGLISH,CHINESE,MATH,SCIENCE,PHYSICS,
              CHEMISTRY,BIOLOGY,COMPUTING,LITERATURE,GENERAL_PAPER,
              POA,MALAY,TAMIL,ECONOMICS,ACCOUNTING,HISTORY,GEOGRAPHY,MUSIC,ART]

# Subject levels
NURSERY_KINDERGARTEN_LEVEL = Constant("Nursery/Kindergarten",r"nursery|kindergarten|k[1-2]")
PRIMARY_LEVEL = Constant("Primary",r"primary [1-6]|p[1-6]|pri|psle")
SECONDARY_LEVEL = Constant("Secondary",r"secondary|sec [1-5]|sec|o-level|o level")
POLYTECHNIC_LEVEL = Constant("Polytechnic",r"poly|polytechnic")
JUNIOR_COLLEGE_LEVEL = Constant("Junior College",r"jc|junior college|jc[1-2]|a-level|a level|h[1-3]")
IB_LEVEL=Constant("IB",r"ib")
IGCSE_LEVEL=Constant("IGCSE",r"igcse")
UNIVERSITY_LEVEL = Constant("University",r"university|uni")
ABRSM = Constant("ABRSM",r"abrsm|grade [1-8]")
## For detail extraction
ALL_SUBJECT_LEVELS:list[Constant] = [NURSERY_KINDERGARTEN_LEVEL,PRIMARY_LEVEL,SECONDARY_LEVEL,
                      POLYTECHNIC_LEVEL,JUNIOR_COLLEGE_LEVEL,
                      IB_LEVEL,IGCSE_LEVEL,UNIVERSITY_LEVEL,
                      ABRSM]

# Address for online tuition
ONLINE_TUITION = Constant("Online","online")

# Gender constants
MALE=Constant("Male",'male')
FEMALE=Constant("Female",'female')
NON_BINARY=Constant("Non-binary",'non-binary')
## For detail extraction
ALL_GENDERS:list[Constant]=[FEMALE,NON_BINARY,MALE]

# Commuting constants for Google Directions API parameters TODO: modify get_directions() method
PUBLIC_TRANSPORT=Constant("Public Transport","transit") # mode=Tutor.PUBLIC_TRANSPORT,transit_mode=["bus","rail"]
DRIVING=Constant("Driving","driving") # mode=Tutor.DRIVING

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
            commute_method:str,
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
# RIAN = Tutor(
#         name="Rian 🪴",
#         telegram_handle="@rianhuii",

#         subjects={MATH,SCIENCE,PHYSICS,CHEMISTRY,COMPUTING},
#         experience={GRADUATE_OR_FULL_TIME},
#         subject_levels={SECONDARY_LEVEL,POLYTECHNIC_LEVEL},

#         address="40B Margaret Drive",
#         gender={MALE},
#         commute_method=PUBLIC_TRANSPORT,
#         max_commute_time=40,
#     )
# MUM = Tutor(
#     name="Mum 🌸",
#     telegram_handle="@Nekotokuma",

#     subjects={ENGLISH,SCIENCE},
#     experience={EX_CURRENT_MOE},
#     subject_levels={PRIMARY_LEVEL,SECONDARY_LEVEL},

#     address="40B Margaret Drive",
#     gender={FEMALE},
#     commute_method=PUBLIC_TRANSPORT,
#     max_commute_time=40,
# )

# Make an importable list
# TUTOR_LIST:list[Tutor] = [
#     RIAN,
#     MUM,
#     Tutor(
#         name="Rachel",
#         telegram_handle="@rachellor",

#         subjects={MATH,ENGLISH,LITERATURE,CHEMISTRY,GENERAL_PAPER},
#         experience={GRADUATE_OR_FULL_TIME},
#         subject_levels={SECONDARY_LEVEL,POLYTECHNIC_LEVEL},

#         address="Sembawang MRT",
#         gender={FEMALE},
#         commute_method=PUBLIC_TRANSPORT,
#         max_commute_time=40,
#     ),
#     Tutor(
#         name="Delia",
#         telegram_handle="@ddxliaa",

#         subjects={MATH},
#         experience={GRADUATE_OR_FULL_TIME},
#         subject_levels={JUNIOR_COLLEGE_LEVEL},

#         address=ONLINE_TUITION,
#         gender={FEMALE},
#         commute_method=None,
#         max_commute_time=None,
#     )
# ]