import requests

from triplan_api.models.trip import Attraction

# Return type: List[Attraction]
def text_search(text_query, latitude, longitude, api_key):
    """
    Calls the Google Maps Places API Text Search.

    :param text_query: Query text (e.g., "Spicy Vegetarian Food in Sydney, Australia")
    :param latitude: Latitude of the central point
    :param longitude: Longitude of the central point
    :param api_key: Google Maps API key
    :return: JSON (up to 20 place_id results)
    """
    url = 'https://places.googleapis.com/v1/places:searchText?languageCode=zh-TW'
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': api_key,
        'X-Goog-FieldMask': 'places.id,places.displayName,places.formattedAddress'
    }
    payload = {
        "textQuery":  " ".join(text_query),
        "locationBias": {
            "circle": {
                "center": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "radius": 10000.0
            }
        },
        "pageSize": 20
    }

    response = requests.post(url, headers=headers, json=payload)

    return response.json()["places"]

'''
locationBias: Tries to return locations within the specified area, with the center defined by latitude and longitude, and radius in meters.
Use pageToken if more than 20 results are needed.
By default, results are sorted by relevance. To sort by distance, add rankPreference.
'''

##############################################################

def place_details(place_id, api_key):
    """
    Calls the Google Maps Places API Place Details.

    :param place_id: Unique ID of the location
    :param api_key: Google Maps API key
    :return: JSON (type, address, rating, URL, review count, name, description, up to five reviews)
    """
    url = f'https://places.googleapis.com/v1/places/{place_id}?languageCode=zh-TW'
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': api_key,
        'X-Goog-FieldMask': 'displayName,types,formattedAddress,rating,googleMapsUri,reviews.text.text,regularOpeningHours,priceLevel,editorialSummary.text,userRatingCount,location'
    }

    response = requests.get(url, headers=headers)
    return response.json()

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
