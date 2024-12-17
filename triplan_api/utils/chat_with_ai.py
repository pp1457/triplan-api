import logging
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage

from triplan_api.models.trip import *
llm = ChatOllama(
    base_url="http://meow1.csie.ntu.edu.tw:11434",
    model="llama3.3",
    temperature=0,
)

# Disable httpx INFO and DEBUG logs (set to WARNING or higher)
logging.getLogger("httpx").setLevel(logging.WARNING)

def acquire_attraction(current_trip, pos_to_put, attractions_list, requirements):
    """
    Function to select the best attraction to place at a specific position in the current trip.

    Parameters:
    - current_trip (list): A list of Attraction objects or None for empty slots.
    - pos_to_put (int): The position in `current_trip` to insert the selected attraction.
    - attractions_list (list): A list of Attraction objects.
    - requirements (str): User's input with additional constraints or preferences.

    Returns:
    - Attraction: The selected attraction object from the `attractions_list`.
    """
    # Prepare descriptions of the current trip and attractions
    current_trip_description = "\n".join(
        f"Position {i + 1}: {attr.name if isinstance(attr, Attraction) else 'Empty slot'}"
        for i, attr in enumerate(current_trip)
    )

    attractions_description = "\n".join(
        f"ID: {i}, Name: {attr.name}, Address: {attr.address}, Visit Duration: {attr.visit_duration} min, "
        f"Rating: {attr.rating or 'N/A'} ({attr.rating_count} reviews), "
        f"Price level: {attr.price_level or 'N/A'}, Tags: {', '.join(attr.tags) if attr.tags else 'None'}, "
        f"Description: {attr.description or 'No description available.'}, "
        f"Reviews: {'; '.join(attr.reviews[:3]) if attr.reviews else 'No reviews available.'}"
        for i, attr in enumerate(attractions_list)
    )

    # Prepare the system and user messages
    system_message = (
        "You are a helpful assistant that picks the best attraction to include in a travel itinerary. "
        "Your goal is to consider the travel smoothness of the trip, avoid unnecessary backtracking, "
        "and ensure the trip is efficient and enjoyable. You will also account for user requirements "
        "and preferences provided as input. Respond only with the ID of the selected attraction."
    )

    human_message = (
        f"Here is the current trip itinerary:\n{current_trip_description}\n\n"
        f"Here is the list of available attractions:\n{attractions_description}\n\n"
        f"The attraction will be placed at position {pos_to_put + 1}.\n"
        f"User requirements: {requirements}\n\n"
        "Based on the above details, which attraction is the best fit for this position? "
        "Respond with only the number (ID of the selected attraction.)"
    )

    # Construct messages for the LLM
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": human_message},
    ]

    # Invoke the LLM
    response = llm.invoke(messages)

    # Extract and validate the selected attraction ID
    selected_id_str = response.content.strip()

    # Convert the response to an integer
    try:
        selected_id = int(selected_id_str)
    except ValueError:
        raise ValueError(
            f"The AI response '{selected_id_str}' is not a valid integer ID. "
            "Please ensure the AI is instructed to respond with a valid ID."
        )

    # Match the selected ID with the attractions list
    if not (0 <= selected_id < len(attractions_list)):
        raise ValueError(
            f"The selected ID '{selected_id}' is out of range. Ensure the response is valid and within the list of attractions."
        )

    return attractions_list[selected_id]
