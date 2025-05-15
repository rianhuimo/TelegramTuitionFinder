
# This class creates the data structure for a tuition channel, along with it's relevant fields
class TuitionChannel():

    def __init__(
            self, 
            channel_name:str, 
            channel_link:str,
            address_regex:str,
            subjects_regex:str,
            subject_levels_regex:str,
            experience_regex:str):
        self.channel_name = channel_name
        self.channel_link = channel_link
        self.address_regex = address_regex
        self.subjects_regex = subjects_regex
        self.subject_levels_regex = subject_levels_regex
        self.experience_regex = experience_regex

TUITION_CHANNEL_LIST = [
    TuitionChannel(
        channel_name="Tuition Assignments Singapore - SG Tuition Jobs / SG Tuition Assignments",
        channel_link="https://t.me/TuitionAssignmentsSG",
        address_regex=r"Address: (.*)",
        subjects_regex=None,
        subject_levels_regex=None,
        experience_regex=None
    ),
    TuitionChannel(
        channel_name="Tuition Assignments Jobs Singapore🇸🇬",
        channel_link="https://t.me/nanyangtuitionjobs",
        address_regex=r"Location/Area: (.*)",
        subjects_regex=None,
        subject_levels_regex=None,
        experience_regex=None
    ),
    TuitionChannel(
        channel_name="🏆 Singapore Tuition Assignments Jobs - sgTuitions",
        channel_link="https://t.me/sgTuitions",
        address_regex=r"@ (.*) \(",
        subjects_regex=None,
        subject_levels_regex=None,
        experience_regex=None
    ),
    TuitionChannel(
        channel_name="Elite Tutor Assignments 🤓",
        channel_link="https://t.me/elitetutorsg",
        address_regex=r"Tuition venue: (.*)",
        subjects_regex=None,
        subject_levels_regex=None,
        experience_regex=None
    ),
    TuitionChannel(
        channel_name="Tuition Assignments Singapore (Ministry of Tuition)",
        channel_link="https://t.me/MinistryofTuitionSG",
        address_regex=r"@ (.*)⚡️",
        subjects_regex=None,
        subject_levels_regex=None,
        experience_regex=None
    ),
    TuitionChannel(
        channel_name="Tuition Jobs (LearnTogether.SG)",
        channel_link="https://t.me/MinistryofTuitionSG",
        address_regex=r"Location: (.*)",
        subjects_regex=None,
        subject_levels_regex=None,
        experience_regex=None
    ),
    TuitionChannel(
        channel_name="🇸🇬 FamilyTutor VIP Assignments 🥇 | Singapore Best Tuition Jobs Portal | SG Tuition Assignments🥇",
        channel_link="https://t.me/FTassignments",
        address_regex=r"@ (.*) \(",
        subjects_regex=None,
        subject_levels_regex=None,
        experience_regex=None
    )
]