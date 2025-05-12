from datetime import datetime
import json
import os
import googlemaps
from dotenv import load_dotenv

load_dotenv()
gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))

now = datetime.now()
directions_result = gmaps.directions(origin="40B Margaret Drive",
                                     destination="Redhill MRT",
                                     mode="transit",
                                     departure_time=now,
                                     transit_mode=["bus","rail"],
                                     alternatives=True)

# sort the possible routes in ascending order
sorted_routes = sorted(directions_result,key=lambda result:result["legs"][0]["duration"]["value"])

with open("route.json","w",encoding="utf-8") as f:
    f.write(str(json.dumps(sorted_routes,indent=2)))

print(json.dumps(directions_result,indent=2))