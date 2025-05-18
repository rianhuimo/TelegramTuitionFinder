import os
from datetime import datetime
from typing import List
from dotenv import load_dotenv
import googlemaps
from classes.tuition_job import TuitionJob
import classes.tutor as Tutor

MAXIMUM_COMMUTE_TIME = 30 # in minutes

load_dotenv()
gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))

def get_directions(
        job_address:str,
        tutor_address:str,
        commute_method:list[str]) -> List[object]:
    # print(f"Getting directions for: {job_address}")
    now = datetime.now()

    # Cleaning up the query
    job_address = job_address.lower().replace("near","")

    try:
        if commute_method == Tutor.PUBLIC_TRANSPORT:
            directions_result = gmaps.directions(origin=f"Singapore {tutor_address}",
                                        destination=f"Singapore {job_address}",
                                        mode="transit",
                                        departure_time=now,
                                        transit_mode=["bus","rail"],
                                        alternatives=True)
        else: # driving is the only alternative to public transport in this logic. Unless you take a bicycle or walk. For now I'm just accommodating for these two transport modes.
            directions_result = gmaps.directions(origin=f"Singapore {tutor_address}",
                                        destination=f"Singapore {job_address}",
                                        mode="transit",
                                        departure_time=now,
                                        transit_mode=["bus","rail"],
                                        alternatives=True)
        # print(json.dumps(directions_result,indent=2))
        if (len(directions_result) > 0):
            # sort the possible routes in ascending order
            sorted_routes = sorted(directions_result,key=lambda result:result["legs"][0]["duration"]["value"])
        else:
            print("⚠️ No directions were found for some reason.")
            sorted_routes = []
        return sorted_routes
        
    except Exception as e:
        print(f"⛔ Error parsing address: {job_address}. Error: {e}")


if (__name__ == "__main__"):
    print("|".join(Tutor.TUTOR_LIST[0].subjects))