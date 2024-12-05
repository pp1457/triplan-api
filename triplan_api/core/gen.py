from triplan_api.utils.chat_with_ai import aquire_attraction
from triplan_api.models.trip import Attraction
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
    Find the middle empty point in the current_trip list.
    Returns the start, end, and mid index (empty point).
    """
    for i in range(1, len(current_trip) - 1):
        if current_trip[i] is None:  # Check for empty slot
            return current_trip[i - 1], current_trip[i + 1], i
    return None, None, None  # No empty points found

# Step 3: Query attractions from a mock data source
def query_attractions(start, end, parsed_input):
    center.lati = (start.location.latitude + end.location.latitude)
    center.long = (start.location.longitude + end.location.longitude)

    for keywords
    candidates = text_search(parsed_input, center.lati, center.long, os.getenv("MAP_API_KEY"))

#def query_attractions(start, end, parsed_input, mid_information):
#    """
#    Mock function to query attractions between start and end.
#    Replace this function with a real query to a service like Google Maps.
#    """
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

# Step 6: Recursive generation
def gen(current_trip, user_input):
    """
    Recursively fill in empty points in the itinerary.
    """
    start, end, mid_index = find_mid_point(current_trip)
    if start is None and end is None:
        print("Trip generation completed!")
        return
    
    # Mock process user input
    parsed_input = process_user_input(user_input)
    mid_information = {"location": current_trip[mid_index - 1]}  # Adjust as needed
    
    # Query attractions
    attractions = query_attractions(start, end, parsed_input, mid_information)
    
    # Use `aquire_attraction` to find the best attraction
    best_attraction = choose_best_attraction(current_trip, mid_index, attractions, user_input)
    
    # Update the trip and recurse
    update_trip(current_trip, mid_index, best_attraction)
    gen(current_trip, user_input)

# Example usage
if __name__ == "__main__":
    # Initialize the trip with Attraction objects and None for empty slots
    current_trip = [
        Attraction(
            name="Home",
            address="Starting Point",
            visit_duration=0,
            travel_time_to_prev=0,
            travel_time_to_next=30,
            tags=["start"],
            description="The starting point of the journey.",
            reviews=[],
            rating=None,
            rating_count=0,
            ticket_price=None,
            url=""
        ),
        None,  # Empty slot to be filled
        Attraction(
            name="Hotel",
            address="Destination",
            visit_duration=0,
            travel_time_to_prev=30,
            travel_time_to_next=0,
            tags=["end"],
            description="The final stop of the journey.",
            reviews=["Comfortable stay!", "Great service."],
            rating=4.5,
            rating_count=150,
            ticket_price=100.0,
            url="http://example.com/hotel"
        ),
    ]

    user_input = "I want to explore historical landmarks and scenic views along the way."
    gen(current_trip, user_input)

    # Print the final trip itinerary
    print("Final trip itinerary:")
    for i, stop in enumerate(current_trip, start=1):
        if isinstance(stop, Attraction):
            print(f"Stop {i}: {stop.name} - {stop.address}")
        elif stop is None:
            print(f"Stop {i}: Empty slot")
