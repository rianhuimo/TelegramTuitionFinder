from datetime import datetime
import json
import os
import re
from typing import List
from dotenv import load_dotenv
import googlemaps
from classes.TuitionJob import TuitionJob
import classes.Tutor as Tutor

MAXIMUM_COMMUTE_TIME = 30 # in minutes

load_dotenv()
gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))

def get_directions(job_address:str, tutor_address:str) -> List[object]:
    print(f"Getting directions for: {job_address}")
    now = datetime.now()
    try:
        directions_result = gmaps.directions(origin=tutor_address,
                                    destination=job_address,
                                    mode="transit",
                                    departure_time=now,
                                    transit_mode=["bus","rail"],
                                    alternatives=True)
        # print(json.dumps(directions_result,indent=2))
        if (len(directions_result) > 0):
            # sort the possible routes in ascending order
            sorted_routes = sorted(directions_result,key=lambda result:result["legs"][0]["duration"]["value"])
        else:
            print("No directions were found for some reason.")
            sorted_routes = []
        return sorted_routes
        
    except Exception as e:
        print(f"⚠️⚠️ Error parsing address: {job_address}. Error: {e}")
   
# Should be a bit more elegant.
def match_tutors(job:TuitionJob) -> List:
    suitable_tutors = []
    for tutor in Tutor.TUTOR_LIST:

        print(f"\nMatching against tutor: {tutor.name}")

        # default values if errors occur
        commute_check = False
        fastest_commute_duration = {
            "text": "1 mins",
            "value": 1,
        }
        subject_match = []
        experience_match = []

        # Filter for location. If the location is too far away from tutor's house, then none of the rest of the filters matter
        
        if job.address == None or job.address == "online":
            commute_check = True # if there was an error parsing the address, still keep the job. It's better to have false positives.
        else:
            try:
                routes = get_directions(job.address,tutor.address)
                fastest_commute_duration = routes[0]["legs"][0]["duration"] # Contains an object with "text" and "value" attributes
                print(f"🗺️ Fastest commute from tutor's address: {fastest_commute_duration["text"]}.")
                commute_check = fastest_commute_duration["value"]/float(60) <= MAXIMUM_COMMUTE_TIME
                print(f"{"✅ Distance seems alright." if (commute_check) else "⛔ That's too far!"}")
            except Exception as e:
                commute_check = True # if there was an error parsing the address, still keep the job. It's better to have false positives.
                print(f"There was an error getting directions: {e}")

        # Filter for subject. Scan the entire message.
        try:
            subject_filter = "|".join(tutor.subjects)
            subject_match = re.findall(subject_filter,job.message,flags=re.IGNORECASE)
            subject_check = len(subject_match) > 0
            if (subject_check): print(f"✅ Matched these subjects for {tutor.name}: {subject_match}")
            else: print(f"⛔ No subjects matched with tutor details: {subject_filter}")
        except Exception as e:
            print(f"There was an error getting subjects: {e}")

        # Filter for experience. Scan the entire message.
        try:
            experience_filter = "|".join(tutor.experience)
            experience_match = re.findall(experience_filter,job.message,flags=re.IGNORECASE)
            experience_check = len(experience_match) > 0
            if (experience_check): print(f"✅ Matched these experiences for {tutor.name}: {experience_match}")
            else: print(f"⛔ No experience matched with tutor details: {experience_filter}")
        except Exception as e:
            print(f"There was an error getting tutor experience: {e}")

        # Filter for level
        try:
            level_filter = "|".join(tutor.level)
            level_match = re.findall(level_filter,job.message,flags=re.IGNORECASE)
            level_check = len(level_match) > 0
            if (level_check): print(f"✅ Matched these levels for {tutor.name}: {level_match}")
            else: print(f"⛔ No levels matched with tutor details: {level_filter}")
        except Exception as e:
            print(f"There was an error getting student level: {e}")

        if (commute_check and subject_check and experience_check and level_check):
            # Tutor is suitable
            suitable_tutors.append([tutor,fastest_commute_duration,subject_match,experience_match,level_match])

    job.suitable_tutors = suitable_tutors



if (__name__ == "__main__"):
    print("|".join(Tutor.TUTOR_LIST[0].subjects))