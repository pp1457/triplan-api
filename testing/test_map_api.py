import json
from triplan_api.utils import map_api as m
from dotenv import load_dotenv
import os

load_dotenv()

# .env 中要有 MAP_API_KEY=your-secret-api-key
api_key = os.getenv("MAP_API_KEY")
print(f"Your 'MAP_API_KEY' is: {api_key}")

# 查詢條件範例
text_query = "台北101"
latitude = 25.0174
longitude = 121.5392
place_id = "ChIJqS4y_ompQjQRZn8d7gQEdSE" #台大
place_id = "ChIJH56c2rarQjQRphD9gvC8BhI"
place_id2 = "ChIJSTLZ6barQjQRMdkCqrP3CNU" #101
travel_mode = "DRIVE"

try:
    results = m.text_search(text_query, latitude, longitude, api_key)
    print("-----------------------------------------------")
    print("text_search result:")
    print(json.dumps(results, indent=4, ensure_ascii=False))
except Exception as e:
    print(f"text_search error: {e}")

try:
    results = m.place_details(place_id, api_key)
    print("-----------------------------------------------")
    print("place_details result:")
    print(json.dumps(results, indent=4, ensure_ascii=False))
except Exception as e:
    print(f"place_details error: {e}")

try:
    results = m.routes(place_id,place_id2,travel_mode,api_key)
    print("-----------------------------------------------")
    print("routes result:")
    print(json.dumps(results, indent=4, ensure_ascii=False))
except Exception as e:
    print(f"routes error: {e}")
