import requests
from datetime import time

from triplan_api.models.trip import Attraction

"""Attraction
    2.name: str
    2.address: str
    1.place_id: str
    1.time_slot: TimeSlot
    2.description: Optional[str] = None
    x.visit_duration: int = 0
    3.travel_time_to_prev: int = 0
    3.travel_time_to_next: int = 0
    x.estimate_start_time: time
    x.estimate_end_time: time
    2.reviews: Optional[List[str]] = None
    2.rating: Optional[float] = None
    2.rating_count: Optional[int] = 0
    x.ticket_price: Optional[float] = None
    x.tags: Optional[List[str]] = None
    2.url: Optional[str] = ""
    2.location: Optional[Location] = None

filled in function: 1.get_attractions 2.place_detail 3.routes x.default
"""

def get_attractions(text_query, latitude, longitude, prev_id, next_id, api_key): 
    """
    Calls the Google Maps Places API Text Search and returns a list of Attractions.

    :param text_query: Query text (e.g., "Spicy Vegetarian Food in Sydney, Australia")
    :param latitude: Latitude of the central point for searching
    :param longitude: Longitude of the central point for searching
    :prev_id: Place_id of previos place
    :next_id: Place_id of next place
    :param api_key: Google Maps API key
    :return: List of Attraction objects
    """
    # API endpoint and headers
    url = 'https://places.googleapis.com/v1/places:searchText?languageCode=zh-TW'
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': api_key,
        'X-Goog-FieldMask': 'places.id'
    }
    
    # Request payload
    payload = {
        "textQuery": text_query,
        "locationBias": {
            "circle": {
                "center": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "radius": 10000.0  # Radius in meters
            }
        },
        "pageSize": 20  # Maximum results
    }

    # API call
    response = requests.post(url, headers=headers, json=payload)
    
    # Handle potential errors
    if response.status_code != 200:
        raise Exception(f"API call failed with status code {response.status_code}: {response.text}")

    # Parse the response
    places = response.json().get("places", [])

    # Create a list of Attraction objects with defaults for missing fields
    attractions = [
        Attraction(
            place_id=place.get("id"),
            name="",  # Default values for required fields
            address="",
            visit_duration=0,
            travel_time_to_prev=0,
            travel_time_to_next=0,
            estimate_start_time=time(0, 0, 0),
            estimate_end_time=time(0, 0, 0)
        )
        for place in places if "id" in place
    ]
    
    # fill more fields
    place_detail(attractions, api_key)

    # fill travel_time
    for attraction in attractions:
        routes_result = routes(prev_id, attraction.place_id, "DRIVE", api_key)
        time_str = routes_result.get('routes', [{}])[0].get('duration', '')
        time_s = int(time_str[:-1])
        h, remainder = divmod(time_s, 3600)
        m, s = divmod(remainder, 60)
        attraction.travel_time_to_prev = time(h, m, s)

        routes_result = routes(attraction.place_id, next_id, "DRIVE", api_key)
        time_str = routes_result.get('routes', [{}])[0].get('duration', '')
        time_s = int(time_str[:-1])
        h, remainder = divmod(time_s, 3600)
        m, s = divmod(remainder, 60)
        attraction.travel_time_to_next = time(h, m, s)

    return attractions

'''
locationBias: Tries to return locations within the specified area, with the center defined by latitude and longitude, and radius in meters.
Use pageToken if more than 20 results are needed.
By default, results are sorted by relevance. To sort by distance, add rankPreference.

transportation defalt as DRIVE.
distance requested but not used.
'''

##############################################################

def place_detail(attractions, api_key):
    """
    Calls the Google Maps Places API Place Details for each attraction and updates their fields.

    :param attractions: List of Attraction objects with place_id already filled
    :param api_key: Google Maps API key
    :return: Integer representing success or failure (1 for success, 0 for failure)
    """
    for attraction in attractions:
        place_id = attraction.place_id
        
        # Construct the URL and headers for the API call
        url = f'https://places.googleapis.com/v1/places/{place_id}?languageCode=zh-TW'
        headers = {
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': api_key,
            'X-Goog-FieldMask': 'displayName,types,formattedAddress,rating,googleMapsUri,reviews.text.text,regularOpeningHours,priceLevel,editorialSummary.text,userRatingCount,location'
        }
        
        # Make the API request
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                # Parse the API response
                data = response.json()
                
                # Update attraction's fields with the API data
                attraction.name = data.get('displayName', {}).get('text','')
                attraction.address = data.get('formattedAddress', '')
                attraction.rating = data.get('rating', None)
                attraction.url = data.get('googleMapsUri', '')
                attraction.reviews = [review.get('text', {}).get('text', '') for review in data.get('reviews', [])]
                attraction.rating_count = data.get('userRatingCount', 0)
                attraction.description = data.get('editorialSummary', {}).get('text', '')
                attraction.location = data.get('location', None)

            else:
                print(f"Error fetching details for place_id {place_id}: {response.status_code}")
                return 0

        except Exception as e:
            print(f"An error occurred while fetching place details for {place_id}: {e}")
            return 0

    return 1

'''
price_level and regularOpeningHours requested, but not used.
'''

##############################################################

def routes(origin_place_id, destination_place_id, travel_mode, api_key):
    """
    Calls the Google Maps Routes API.
    
    :param origin_place_id: Place ID of the starting location
    :param destination_place_id: Place ID of the destination
    :param travel_mode: Mode of transportation ("DRIVE", "BICYCLE", "WALK", "TRANSIT", "TWO_WHEELER")
    :param api_key: Google Maps API key
    :return: JSON (time in seconds, distance in meters)
    """
    url = 'https://routes.googleapis.com/directions/v2:computeRoutes?languageCode=zh-TW'
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': api_key,
        'X-Goog-FieldMask': 'routes.duration,routes.distanceMeters'
    }
    data = {
        "origin": {
            "placeId": origin_place_id
        },
        "destination": {
            "placeId": destination_place_id
        },
        "travelMode": travel_mode
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

##############################################################

def get_place_id(text_query, api_key):
    """
    Calls the Google Maps Places API Text Search to get place_id.

    :param text_query: Query text
    :param api_key: Google Maps API key
    :return: place_id (None for failure)
    """
    url = 'https://places.googleapis.com/v1/places:searchText?languageCode=zh-TW'
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': api_key,
        'X-Goog-FieldMask': 'places.id'
    }
    payload = {
        "textQuery": text_query,
        "pageSize": 1
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data.get('places', [])[0].get('id','')

    else:
        print(f"Error with response.status_code: {response.status_code}")
        return None

##############################################################

def get_location(place_id, api_key):
    """
    Calls the Google Maps Places API Text Search to get location.

    :param place_id: Unique ID of the location
    :param api_key: Google Maps API key
    :return: location (None for failure)
    """
    url = f'https://places.googleapis.com/v1/places/{place_id}?languageCode=zh-TW'
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': api_key,
        'X-Goog-FieldMask': 'displayName,types,formattedAddress,rating,googleMapsUri,reviews.text.text,regularOpeningHours,priceLevel,editorialSummary.text,userRatingCount,location'
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    return data.get('location', None)
