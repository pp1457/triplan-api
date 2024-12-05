from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage

from triplan_api.models.trip import *

llm = ChatOllama(
    model="llama3.1",
    temperature=0,
)

def aquire_attraction(current_trip, pos_to_put, attractions_list, requirements):
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
        f"- Name: {attr.name}, Location: {attr.location}, Visit Duration: {attr.visit_duration} min, "
        f"Score: {attr.score or 'N/A'}, Tags: {', '.join(attr.tags) if attr.tags else 'None'}"
        for attr in attractions_list
    )

    # Prepare the system and user messages
    system_message = (
        "You are a helpful assistant that picks the best attraction to include in a travel itinerary. "
        "Your goal is to consider the travel smoothness of the trip, avoid unnecessary backtracking, "
        "and ensure the trip is efficient and enjoyable. You will also account for user requirements "
        "and preferences provided as input. Respond only with the name of the selected attraction."
    )

    human_message = (
        f"Here is the current trip itinerary:\n{current_trip_description}\n\n"
        f"Here is the list of available attractions:\n{attractions_description}\n\n"
        f"The attraction will be placed at position {pos_to_put + 1}.\n"
        f"User requirements: {requirements}\n\n"
        "Based on the above details, which attraction is the best fit for this position? "
        "Respond with only the name of the selected attraction."
    )

    # Construct messages for the LLM
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": human_message},
    ]

    # Invoke the LLM
    response = llm.invoke(messages)

    # Extract and validate the selected attraction name
    selected_name = response.content.strip()
    print(f"AI Response: {selected_name}")

    # Match the selected name with the attractions list
    selected_attraction = next(
        (attr for attr in attractions_list if attr.name.lower() == selected_name.lower()), None
    )

    if selected_attraction is None:
        raise ValueError(
            f"The AI selected '{selected_name}', which does not match any attraction in the provided list. "
            "Please ensure the AI response is accurate and corresponds to a valid attraction name."
        )

    return selected_attraction
