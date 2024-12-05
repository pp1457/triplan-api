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

# Check if a parameter is passed
if len(sys.argv) != 2:
    print("Usage: python3 -m testing.test_map_api <parameter>")
    print("Parameters:")
    print("1 - text_search")
    print("2 - place_details")
    print("3 - routes")
    sys.exit(1)

parameter = sys.argv[1]

# Default values
default_text_query = "台北 咖啡廳"
default_latitude = 25.0174
default_longitude = 121.5392
default_place_id = "ChIJH56c2rarQjQRphD9gvC8BhI"
default_origin_place_id = "ChIJqS4y_ompQjQRZn8d7gQEdSE"  # 台大
default_destination_place_id = "ChIJSTLZ6barQjQRMdkCqrP3CNU"  # 101
default_travel_mode = "DRIVE"

print("press enter for defalt parameter")

# Execute corresponding function based on the parameter
if parameter == "1":
    # text_search
    text_query = input(f"Please input text_query (default {default_text_query}): ") or default_text_query
    latitude_input = input(f"Please input latitude (default {default_latitude}): ") or default_latitude
    longitude_input = input(f"Please input longitude (default {default_longitude}): ") or default_longitude
    try:
        latitude = float(latitude_input)
        longitude = float(longitude_input)
        results = m.text_search(text_query, latitude, longitude, api_key)
        print("-----------------------------------------------")
        print("text_search result:")
        print(json.dumps(results, indent=4, ensure_ascii=False))
    except Exception as e:
        print(f"text_search error: {e}")

elif parameter == "2":
    # place_details
    place_id = input(f"Please input place_id (default {default_place_id}): ") or default_place_id
    try:
        results = m.place_details(place_id, api_key)
        print("-----------------------------------------------")
        print("place_details result:")
        print(json.dumps(results, indent=4, ensure_ascii=False))
    except Exception as e:
        print(f"place_details error: {e}")

elif parameter == "3":
    # routes
    origin_place_id = input(f"Please input origin_place_id (default {default_origin_place_id}): ") or default_origin_place_id
    destination_place_id = input(f"Please input destination_place_id (default {default_destination_place_id}): ") or default_destination_place_id
    travel_mode = input(f"Please input travel_mode (e.g., DRIVE, WALK, default {default_travel_mode}): ").upper() or default_travel_mode
    try:
        results = m.routes(origin_place_id, destination_place_id, travel_mode, api_key)
        print("-----------------------------------------------")
        print("routes result:")
        print(json.dumps(results, indent=4, ensure_ascii=False))
    except Exception as e:
        print(f"routes error: {e}")

else:
    print("Usage: python script.py <parameter>")
    print("Parameters:")
    print("1 - text_search")
    print("2 - place_details")
    print("3 - routes")
