
# This class creates the data structure for a tuition channel, along with it's relevant fields
class TuitionChannel():

    def __init__(self, channel_name:str, address_filter:str, channel_link:str):
        self.channel_name = channel_name
        self.address_filter = address_filter
        self.channel_link = channel_link

TUITION_CHANNEL_LIST = [
    TuitionChannel(
        "Tuition Assignments Singapore - SG Tuition Jobs / SG Tuition Assignments",
        r"Address: (.*)",
        "https://t.me/TuitionAssignmentsSG"
    ),
    TuitionChannel(
        "Tuition Assignments Jobs Singapore🇸🇬",
        r"Location/Area: (.*)",
        "https://t.me/nanyangtuitionjobs"
    ),
    TuitionChannel(
        "🏆 Singapore Tuition Assignments Jobs - sgTuitions",
        r"@ (.*) \(",
        "https://t.me/sgTuitions"
    ),
    TuitionChannel(
        "Elite Tutor Assignments 🤓",
        r"Tuition venue: (.*)",
        "https://t.me/elitetutorsg"
    ),
    TuitionChannel(
        "Tuition Assignments Singapore (Ministry of Tuition)",
        r"@ (.*)⚡️",
        "https://t.me/MinistryofTuitionSG",
    ),
    TuitionChannel(
        "Tuition Jobs (LearnTogether.SG)",
        r"Location: (.*)",
        "https://t.me/MinistryofTuitionSG",
    ),
    TuitionChannel(
        "🇸🇬 FamilyTutor VIP Assignments 🥇 | Singapore Best Tuition Jobs Portal | SG Tuition Assignments🥇",
        r"@ (.*) \(",
        "https://t.me/FTassignments",
    )
]