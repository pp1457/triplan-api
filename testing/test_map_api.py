# \triplan-api> python3 -m testing.test_map_api

import json
from triplan_api.utils import map_api as m
from dotenv import load_dotenv
import os
import sys

load_dotenv()

# Read API key from .env
api_key = os.getenv("MAP_API_KEY")

if not api_key:
    print("Error: MAP_API_KEY is not set in .env file.")
    sys.exit(1)

text_query = "台北 咖啡廳"
latitude = 25.0174
longitude = 121.5392
place_id = "ChIJqS4y_ompQjQRZn8d7gQEdSE"  # 台大
prev_id = "ChIJqS4y_ompQjQRZn8d7gQEdSE"  # 台大
next_id = "ChIJSTLZ6barQjQRMdkCqrP3CNU"  # 101

#test get_place_id
print(f"place_id: {m.get_place_id("臺大", api_key)}")

#test get_location
print(f"location: {m.get_location(place_id, api_key)}")

#test get_attractions
attractions = m.get_attractions(text_query, latitude, longitude, prev_id, next_id, api_key)

print(f"Number of attractions: {len(attractions)}\n")

# details of first attraction
if attractions:
    first_attraction = attractions[0]
    print(f"First attraction details:")
    print('------------------------------')
    for key, value in first_attraction.__dict__.items():
        if key == "reviews" and isinstance(value, list):
            print(f"{key}: 我遮掉了，想看自己去test開")
            #print(f"{key}: ")
            #for review in value:
            #    print(f"{review}")
        else:
            print(f"{key}: {value}")
    print('------------------------------')
else:
    print("No attractions found.")
