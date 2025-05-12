from datetime import datetime
import os
import re
from typing import List
from dotenv import load_dotenv
import googlemaps
import Tutor

load_dotenv()
gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))

TUITION_CHANNEL_REGEX_MATCHER = {
    "Tuition Assignments Singapore - SG Tuition Jobs / SG Tuition Assignments": {
        "subject": r"Subject: (.*)",
        "address": r"Address: (.*)",
        "experience": r"\n\((.*)\)\nSubject",
    },
    "Tuition Assignments Jobs Singapore🇸🇬":{
        "subject": r"Level and Subject\(s\): (.*)",
        "address": r"Location/Area: (.*)",
        "experience": r"Looking for (.*) to teach",
    },
    "🏆 Singapore Tuition Assignments Jobs - sgTuitions":{
        "subject": r"Info: (.*) @",
        "address": r"@ (.*) \("
    },
    "Elite Tutor Assignments 🤓":{
        "subject": r"Subject: (.*)",
        "address": r"Tuition venue: (.*)",
        "experience":r"Tutor requirement: (.*)"
    },
    "Tuition Assignments Singapore (Ministry of Tuition)":{
        "subject": r"⚡️(.*) @",
        "address": r"@ (.*)⚡️"
    },
}

def get_tuition_details(message:str,tuition_channel:str) -> object:
    # get the subject and address of the tuition assignment

    subjects = "unknown"
    address = "unknown"
    experience = "unknown"

    try:
        subjects = re.findall(TUITION_CHANNEL_REGEX_MATCHER[tuition_channel]["subject"],message)
        address = re.findall(TUITION_CHANNEL_REGEX_MATCHER[tuition_channel]["address"],message)[0]

        # this part's tricky as the syntax is quite loose...
        if("experience" in TUITION_CHANNEL_REGEX_MATCHER[tuition_channel]):
            print(f"Using regex pattern: {TUITION_CHANNEL_REGEX_MATCHER[tuition_channel]["experience"]}")
            experience = re.findall(TUITION_CHANNEL_REGEX_MATCHER[tuition_channel]["experience"],message)
        else:
            experience = re.findall(r"Student tutor|full-time|full time|part-time|part time|EX/CURRENT MOE|MOE current/ex|Ex-MOE|Current MOE|MOE NIE Teachers",
                message,flags=re.IGNORECASE)
    except Exception as e:
        print(f"Error parsing details: {e}")

    return {
        "subjects":subjects,
        "address":address,
        "experience":experience,
    }

# This function takes in the details of the tuition job, and matches them against the attributes of the list of tutors provided.
# The function outputs a modified version of the job, but with a new field, specifiying the suitable tuitors for the job
def match_suitable_tutors(tuition_job:object) -> object:
    print("🔍 Filtering.............")

    suitable_tutors = []
    for tutor in Tutor.TUTOR_LIST:
        print(f"\nFiltering for {tutor.name}:")

        # filter for subject
        subject_filter = "|".join(tutor.subjects)
        subject_values = ",".join(tuition_job["subjects"])
        subject_match = re.findall(subject_filter,subject_values,flags=re.IGNORECASE)
        subject_check = len(subject_match) > 0
        
        # filter for experience
        experience_filter = "|".join(tutor.experience)
        experience_values = ",".join(tuition_job["experience"])
        experience_match = re.findall(experience_filter,experience_values,flags=re.IGNORECASE)
        experience_check = len(experience_match) > 0

        # filter for gender check
        gender_check = False #TODO: replace with regex pattern match

        # Filter for location. If the location is too far away from tutor's house, then none of the rest of the filters matter
        maximum_commute_time = 45
        routes = get_directions(tuition_job["address"],tutor.address)
        fastest_commute_duration = routes[0]["legs"][0]["duration"] # Contains an object with "text" and "value" attributes
        print(f"Fastest commute from tutor's address: {fastest_commute_duration["text"]}")

        
        if (subject_check and experience_check and fastest_commute_duration["value"]/float(60) <= maximum_commute_time): # Maxium 
            # Add the tutor to the list of suitable tutors
            suitable_tutors.append({
                "name":tutor.name,
                "subject_match":subject_match,
                "experience_match":experience_match,
                "fastest_commute_duration":fastest_commute_duration
            })
            # Print logging
            print(f"[{subject_check}] Matched these subjects for {tutor.name}: {subject_match}")
            print(f"[{experience_check}] Matched these experiences for {tutor.name}: {experience_match}")




    tuition_job = {
                **tuition_job,
                "suitable_tutors": suitable_tutors
    }

    return tuition_job

def get_directions(job_address:str, tutor_address:str) -> List[object]:
    print(f"Getting directions for: {job_address}")
    now = datetime.now()
    directions_result = gmaps.directions(origin=tutor_address,
                                     destination=job_address,
                                     mode="transit",
                                     departure_time=now,
                                     transit_mode=["bus","rail"],
                                     alternatives=True)
    
    # sort the possible routes in ascending order
    sorted_routes = sorted(directions_result,key=lambda result:result["legs"][0]["duration"]["value"])
    return sorted_routes

if (__name__ == "__main__"):
    print("|".join(Tutor.TUTOR_LIST[0].subjects))