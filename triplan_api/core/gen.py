import os

from datetime import time
from dotenv import load_dotenv

from triplan_api.utils.chat_with_ai import aquire_attraction
from triplan_api.models.trip import Attraction, Location, EmptySpot, TimeSlot
from triplan_api.utils.map_api import *

# Step 1: Mock process_user_input
def process_user_input(user_input):
    """
    Mock function to process the user's input.
    Instead of interacting with an AI or API, return a simple parsed value for testing.
    """
    return f"Mocked parsed input for: {user_input}"

# Step 2: Find the middle empty point
def find_mid_point(current_trip):
    """
    Find the middle point of a consecutive subarray of empty (None) slots in the current_trip list.
    Returns the previous non-None value, the next non-None value, and the index of the middle empty point.
    """
    n = len(current_trip)
    i = 0
    results = (None, None, None, None)

    while i < n:
        if isinstance(current_trip[i], EmptySpot):  # Start of a None sequence
            start = i
            # Find the end of this None sequence
            while i < n and isinstance(current_trip[i], EmptySpot):
                i += 1
            end = i - 1

            # Calculate the middle index of the None sequence
            mid_index = (start + end) // 2
            # Get previous and next non-None values
            prev_non_none = current_trip[start - 1] if start > 0 else None
            next_non_none = current_trip[end + 1] if end + 1 < n else None

            results = (prev_non_none, next_non_none, current_trip[mid_index], mid_index)
            break
        else:
            i += 1

    return results

# Step 3: Query attractions from a mock data source
def query_attractions(target, start, end, parsed_input):
    center = Location
    center.lati = (start.location.latitude + end.location.latitude) / 2
    center.long = (start.location.longitude + end.location.longitude) / 2

    load_dotenv()
    api_key = os.getenv("MAP_API_KEY")

    candidates = text_search(parsed_input[target.time_slot], center.lati, center.long, api_key)

    attractions = []

    travel_modes = ["DRIVE", "BICYCLE", "WALK", "TRANSIT", "TWO_WHEELER"]

    for candidate in candidates:
        attraction = place_details(candidate["id"], api_key)
        attraction.travel_time_to_prev = routes(start.place_id, attraction.place_id, "WALK", api_key)
        attraction.travel_time_to_next = routes(attraction.place_id, end.place_id, "WALK", api_key)
        attractions.append(attraction)

    return attractions

#def query_attractions(target, start, end, parsed_input):
#    """
#    Mock function to query attractions between start and end.
#    Replace this function with a real query to a service like Google Maps.
#    """
#    
#    attractions = [
#        Attraction(
#            name="Museum of History",
#            address="City Center",
#            visit_duration=120,
#            travel_time_to_prev=0,
#            travel_time_to_next=30,
#            tags=["historical"],
#            description="A museum showcasing the history of the city.",
#            reviews=["Amazing artifacts!", "Very informative."],
#            rating=4.8,
#            rating_count=200,
#            ticket_price=15.0,
#            url="http://example.com/museum"
#        ),
#        Attraction(
#            name="Scenic Park",
#            address="Near River",
#            visit_duration=90,
#            travel_time_to_prev=30,
#            travel_time_to_next=30,
#            tags=["scenic", "relaxing"],
#            description="A peaceful park with beautiful river views.",
#            reviews=["Perfect for a stroll.", "Great place to relax."],
#            rating=4.5,
#            rating_count=150,
#            ticket_price=5.0,
#            url="http://example.com/park"
#        ),
#        Attraction(
#            name="Art Gallery",
#            address="Downtown",
#            visit_duration=60,
#            travel_time_to_prev=15,
#            travel_time_to_next=20,
#            tags=["art", "cultural"],
#            description="A gallery featuring contemporary art.",
#            reviews=["Impressive collection!", "A must-visit for art lovers."],
#            rating=4.7,
#            rating_count=180,
#            ticket_price=10.0,
#            url="http://example.com/gallery"
#        ),
#    ]
#    return attractions

# Step 4: Use `aquire_attraction` to choose the best attraction
def choose_best_attraction(current_trip, mid_index, attractions, user_input):
    """
    Select the best attraction using the aquire_attraction function.
    """
    return aquire_attraction(current_trip, mid_index, attractions, user_input)

# Step 5: Update the current_trip with the best attraction
def update_trip(current_trip, mid_index, best_attraction):
    """
    Update the current_trip list with the best attraction at the midpoint.
    """
    current_trip[mid_index] = best_attraction

def find_place_id(place):
    load_dotenv()
    api_key = os.getenv("MAP_API_KEY")
    result = text_search(place.address if place.address != None else place.name, -1, -1, api_key)
    place.place_id = result["places"][0]["id"]
    if place.address is None:
        place.address = result["places"][0]["address"]
    return place

# Step 6: Recursive generation
def gen(current_trip, parsed_input):
    """
    Recursively fill in empty points in the itinerary.
    """

    start, end, mid, mid_index = find_mid_point(current_trip)
    if start.place_id == None:
        start = find_place_id(start)
    if end.place_id == None:
        end = find_place_id(end)


    if start is None and end is None:
        print("Trip generation completed!")
        return
    
    # Mock process user input
    
    # Query attractions
    attractions = query_attractions(mid, start, end, parsed_input)

    
    # Use `aquire_attraction` to find the best attraction
    best_attraction = choose_best_attraction(current_trip, mid_index, attractions, user_input)
    
    # Update the trip and recurse
    update_trip(current_trip, mid_index, best_attraction)
    gen(current_trip, user_input)

    return current_trip

# Example usage
if __name__ == "__main__":
    # Initialize the trip with Attraction objects and None for empty slots
    current_trip = [
        Attraction(
            name="Home",
            address="Starting Point",
            place_id="123",
            time_slot=TimeSlot.MORNING,
            visit_duration=0,
            travel_time_to_prev=0,
            travel_time_to_next=30,
            estimate_start_time=time(8, 0),
            estimate_end_time=time(8, 0),
            tags=["start"],
            description="The starting point of the journey.",
            reviews=[],
            rating=None,
            rating_count=0,
            ticket_price=None,
            url="",
            location=Location(latitude=40.7128, longitude=-74.0060)  # Example coordinates for New York City
        ),
        EmptySpot(
            time_slot=TimeSlot.AFTERNOON,
            estimate_start_time=time(10, 0),
            estimate_end_time=time(12, 0)
        ),
        Attraction(
            name="Hotel",
            address="Destination",
            place_id="123",
            time_slot=TimeSlot.NIGHT,
            visit_duration=0,
            travel_time_to_prev=30,
            travel_time_to_next=0,
            estimate_start_time=time(23, 0),
            estimate_end_time=time(23, 0),
            tags=["end"],
            description="The final stop of the journey.",
            reviews=["Comfortable stay!", "Great service."],
            rating=4.5,
            rating_count=150,
            ticket_price=100.0,
            url="http://example.com/hotel",
            location=Location(latitude=48.8566, longitude=2.3522)  # Example coordinates for Paris
        )
    ]

    user_input = {
        "morning": ["coffee", "toast", "eggs", "exercise"],
        "night": ["rest", "relax", "movie", "sleep"],
        "breakfast": ["cereal", "pancakes", "fruit", "yogurt"],
        "lunch": ["sandwich", "salad", "soup", "fruit"],
        "afternoon": ["coffee", "snack", "work", "study"],
        "dinner": ["pasta", "steak", "salad", "vegetables"]
    }
    gen(current_trip, user_input)

    # Print the final trip itinerary
    print("Final trip itinerary:")
    for i, stop in enumerate(current_trip, start=1):
        if isinstance(stop, Attraction):
            print(f"Stop {i}: {stop.name} - {stop.address}")
        elif stop is None:
            print(f"Stop {i}: Empty slot")
