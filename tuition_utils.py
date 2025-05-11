import re

TUITION_CHANNEL_REGEX_MATCHER = {
    "Tuition Assignments Singapore - SG Tuition Jobs / SG Tuition Assignments": {
        "subject": r"Subject: (.*)",
        "address": r"Address: (.*)"
    },
    "Tuition Assignments Jobs Singapore🇸🇬":{
        "subject": r"Level and Subject\(s\): (.*)",
        "address": r"Location/Area: (.*)"
    },
    "🏆 Singapore Tuition Assignments Jobs - sgTuitions":{
        "subject": r"Info: (.*) @",
        "address": r"@ (.*) \("
    },
    "Elite Tutor Assignments 🤓":{
        "subject": r"Subject: (.*)",
        "address": r"Tuition venue: (.*)"
    },
    "Tuition Assignments Singapore (Ministry of Tuition)":{
        "subject": r"⚡️(.*) @",
        "address": r"@ (.*)⚡️"
    },
}

def get_tuition_details(message:str,tuition_channel:str) -> object:
    # get the subject and address of the tuition assignment

    subject = "unknown"
    address = "unknown"
    matches_experience = "unknown"

    try:
        subject = re.findall(TUITION_CHANNEL_REGEX_MATCHER[tuition_channel]["subject"],message)
        address = re.findall(TUITION_CHANNEL_REGEX_MATCHER[tuition_channel]["address"],message)
        matches_experience = re.findall(r"full-time|full time|part-time|part time",message,flags=re.IGNORECASE)
    except:
        print("Error parsing details")

    return [subject,address,matches_experience]