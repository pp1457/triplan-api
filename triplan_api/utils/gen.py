from triplan_api.utils.chat_with_ai import aquire_attraction
from triplan_api.models.trip import Attraction


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
def query_attractions(start, end, parsed_input, mid_information):
    """
    Mock function to query attractions between start and end.
    Replace this function with a real query to a service like Google Maps.
    """
    attractions = [
        Attraction(name="Museum of History", location="City Center", visit_duration=120, score=4.8, tags=["historical"]),
        Attraction(name="Scenic Park", location="Near River", visit_duration=90, score=4.5, tags=["scenic", "relaxing"]),
        Attraction(name="Art Gallery", location="Downtown", visit_duration=60, score=4.7, tags=["art", "cultural"]),
    ]
    return attractions

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
            location="Starting Point",
            visit_duration=0,
            score=0,
            tags=["start"],
            travel_time_to_prev=0,
            travel_time_to_next=30
        ),
        None,  # Empty slot to be filled
        Attraction(
            name="Hotel",
            location="Destination",
            visit_duration=0,
            score=0,
            tags=["end"],
            travel_time_to_prev=30,
            travel_time_to_next=0
        ),
    ]

    user_input = "I want to explore historical landmarks and scenic views along the way."
    gen(current_trip, user_input)

    # Print the final trip itinerary
    print("Final trip itinerary:")
    for i, stop in enumerate(current_trip, start=1):
        if isinstance(stop, Attraction):
            print(f"Stop {i}: {stop.name} - {stop.location}")
        elif stop is None:
            print(f"Stop {i}: Empty slot")
