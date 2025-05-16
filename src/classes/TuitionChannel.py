
# This class creates the data structure for a tuition channel, along with it's relevant fields
class TuitionChannel():

    def __init__(
            self, 
            channel_name:str, 
            channel_link:str,
            address_regex:str,
            subjects_regex:str,
            subject_levels_regex:str,
            experience_regex:str,
            gender_preference_regex:str):
        self.channel_name = channel_name
        self.channel_link = channel_link
        self.address_regex = address_regex
        self.subjects_regex = subjects_regex
        self.subject_levels_regex = subject_levels_regex
        self.experience_regex = experience_regex
        self.gender_preference_regex = gender_preference_regex # If no preference, regex will return []

TUITION_CHANNEL_LIST = [
    TuitionChannel(
        channel_name="Tuition Assignments Singapore - SG Tuition Jobs / SG Tuition Assignments",
        channel_link="https://t.me/TuitionAssignmentsSG",
        address_regex=r"Address: (.*)",
        subjects_regex=r"Subject: (.*)",
        subject_levels_regex=r"Subject: (.*)",
        experience_regex=r"\((.*) Tutor\)",
        gender_preference_regex=r"\((.*) Tutor\)"
    ),
    TuitionChannel(
        channel_name="Tuition Assignments Jobs Singapore🇸🇬",
        channel_link="https://t.me/nanyangtuitionjobs",
        address_regex=r"Location/Area: (.*)",
        subjects_regex=r"Level and Subject\(s\): (.*)",
        subject_levels_regex=r"Level and Subject\(s\): (.*)",
        experience_regex=r"Hourly Rate: (.*)|Parent prefers to engage a (.*)",
        gender_preference_regex=r"Remarks: Tutors who include their relevant teaching experience in details have higher success rate of being engaged by the parent\.\n\n"
    ),
    TuitionChannel(
        channel_name="🏆 Singapore Tuition Assignments Jobs - sgTuitions",
        channel_link="https://t.me/sgTuitions",
        address_regex=r"@ (.*) \(",
        subjects_regex=r"Info: (.*)|Hashtags: (.*)",
        subject_levels_regex=r"Info: (.*)|Hashtags: (.*)",
        experience_regex=r"Tutor Types: (.*)",
        gender_preference_regex=None # not set in stone. Sometimes mentions the student's gender and not their gender preference (troublesome)
    ),
    TuitionChannel(
        channel_name="Elite Tutor Assignments 🤓",
        channel_link="https://t.me/elitetutorsg",
        address_regex=r"Tuition venue: (.*)",
        subjects_regex=r"Subject: (.*)",
        subject_levels_regex=r"Subject: (.*)",
        experience_regex=r"Tutor requirement: (.*)",
        gender_preference_regex=None # Can't find any. Will code the function to accommodate for no gender filters, translates to: Tutor.gender_preferences=None
    ),
    TuitionChannel(
        channel_name="Tuition Assignments Singapore (Ministry of Tuition)",
        channel_link="https://t.me/MinistryofTuitionSG",
        address_regex=r"@ (.*)⚡️",
        subjects_regex=r"⚡️(.*) @",
        subject_levels_regex=r"⚡️(.*) @",
        experience_regex=r"Remarks: (.*)|Preference: (.*)",
        gender_preference_regex=r"Remarks: (.*)|Preference: (.*)"
    ),
    TuitionChannel(
        channel_name="Tuition Jobs (LearnTogether.SG)",
        channel_link="https://t.me/MinistryofTuitionSG",
        address_regex=r"Location: (.*)",
        subjects_regex=r"Subject: (.*)",
        subject_levels_regex=r"Subject: (.*)",
        experience_regex=r"Fees: (.*)|Remarks: (.*)",
        gender_preference_regex=r"Tutor Preference: (.*)|Remarks: (.*)"
    ),
    TuitionChannel(
        channel_name="🇸🇬 FamilyTutor VIP Assignments 🥇 | Singapore Best Tuition Jobs Portal | SG Tuition Assignments🥇",
        channel_link="https://t.me/FTassignments",
        address_regex=r"@ (.*) \(",
        subjects_regex=r"Info: (.*)|Hashtags: (.*)",
        subject_levels_regex=r"Info: (.*)|Hashtags: (.*)",
        experience_regex=r"Tutor Types: (.*)",
        gender_preference_regex=None # not set in stone. Sometimes mentions the student's gender and not their gender preference (troublesome)
    )
]