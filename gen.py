from langchain.chat_models import ChatOpenAI  # For LangChain
import googlemaps  # For Google Maps API integration

# Initialize Google Maps API client (replace YOUR_API_KEY with your actual key)
gmaps = googlemaps.Client(key="YOUR_API_KEY")

# Step 1: Process user input
def process_user_input(user_input):
    """
    Use an LLM to process the user's input and make it friendly for the Google Maps API.
    """
    llm = ChatOpenAI(model="ollama", temperature=0)  # Replace "ollama" with production model as needed
    prompt = f"Convert the following user request into a format suitable for the Google Maps API:\n\n{user_input}"
    parsed_input = llm.generate(prompt)  # Use LangChain to process the input
    return parsed_input.strip()

# Step 2: Find the middle empty point
def find_mid_point(current_trip):
    """
    Find the middle empty point in the current_trip list.
    Returns the start, end, and mid (empty point).
    """
    for i in range(1, len(current_trip) - 1):
        if not current_trip[i]:  # Check for empty point
            return current_trip[i - 1], current_trip[i + 1], i
    return None, None, None  # No empty points found

# Step 3: Query Google Maps
def ask_google(start, end, parsed_input, mid_information):
    """
    Query Google Maps API for attractions between start and end based on parsed input.
    """
    response = gmaps.places_nearby(
        location=mid_information["location"],  # Midpoint location (e.g., GPS coordinates)
        keyword=parsed_input,
        radius=5000  # Search within 5km
    )
    attractions = response.get("results", [])
    return attractions

# Step 4: Use AI to choose the best attraction
def ask_ai(attractions, user_input, mid_information):
    """
    Use LangChain (or other LLM) to rank and choose the best attraction.
    """
    llm = ChatOpenAI(model="ollama", temperature=0)
    prompt = f"""
    Here is a list of attractions with details:\n\n{attractions}\n\n
    User's preferences:\n\n{user_input}\n\n
    Midpoint details:\n\n{mid_information}\n\n
    Rank the attractions and choose the best one.
    """
    response = llm.generate(prompt)
    return response.strip()

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
    
    # Process user input and query Google Maps
    parsed_input = process_user_input(user_input)
    mid_information = {"location": current_trip[mid_index - 1]}  # Adjust as needed
    attractions = ask_google(start, end, parsed_input, mid_information)
    
    # Use AI to find the best attraction
    best_attraction = ask_ai(attractions, user_input, mid_information)
    
    # Update the trip and recurse
    update_trip(current_trip, mid_index, best_attraction)
    gen(current_trip, user_input)

# Example usage
if __name__ == "__main__":
    current_trip = ["Home", None, "Hotel"]  # Example trip with an empty midpoint
    user_input = "I want to explore historical landmarks and scenic views along the way."
    gen(current_trip, user_input)
    print("Final trip itinerary:", current_trip)
