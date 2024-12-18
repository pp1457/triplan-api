import logging
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage

from triplan_api.models.trip import *

# Initialize LLM
llm = ChatOllama(
    base_url="http://meow1.csie.ntu.edu.tw:11434",
    model="llama3.1",
    temperature=0,
)

# Disable httpx INFO and DEBUG logs, keeping only WARNING or higher
logging.getLogger("httpx").setLevel(logging.WARNING)

def acquire_attraction(current_trip, pos_to_put, attractions_list, requirements):
    """
    Select the best attraction to insert at a specific position in the current trip.

    Parameters:
    - current_trip (list): The current trip, with each element being an Attraction object or None (empty slots).
    - pos_to_put (int): The index in `current_trip` where the attraction will be inserted.
    - attractions_list (list): A list of Attraction objects available for selection.
    - requirements (str): User preferences and constraints (e.g., preferred types or time requirements).

    Returns:
    - Attraction: The selected attraction object.
    """
    # Prepare the current trip description
    current_trip_description = "\n".join(
        f"位置 {i + 1}: {attr.name if isinstance(attr, Attraction) else '空時段'}"
        for i, attr in enumerate(current_trip)
    )

    # Prepare the attractions list description
    attractions_description = "\n".join(
        f"ID: {i}, 名稱: {attr.name}, 地址: {attr.address}, 參觀時長: {attr.visit_duration} 分鐘, "
        f"評分: {attr.rating or 'N/A'} （{attr.rating_count} 則評論）, "
        f"價格等級: {attr.price_level or 'N/A'}, 標籤: {', '.join(attr.tags) if attr.tags else '無標籤'}, "
        f"描述: {attr.description or '無描述'}, "
        f"評論: {'; '.join(attr.reviews[:3]) if attr.reviews else '無評論'}"
        for i, attr in enumerate(attractions_list)
    )

    # System message (in Chinese)
    system_message = (
        "你是一個行程規劃助手，負責選擇最適合加入行程的景點。你的目標是：\n"
        "1. 確保行程順暢，避免不必要的往返。\n"
        "2. 提高行程效率和愉悅度。\n"
        "3. 同時考慮使用者的需求和偏好。\n"
        "你的回應應該僅包含被選景點的 ID 數字。"
    )

    # User message (in Chinese)
    human_message = (
        f"以下是目前的行程：\n{current_trip_description}\n\n"
        f"以下是可選景點清單：\n{attractions_description}\n\n"
        f"將選擇的景點放在行程中的第 {pos_to_put + 1} 個位置。\n"
        f"使用者需求：{requirements}\n\n"
        "根據以上資訊，哪個景點最適合放在該位置？請僅以該景點的 ID 數字作為回應。"
    )

    # Construct messages for LLM
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
            "Ensure the AI is instructed to respond with a valid ID."
        )

    # Check if the selected ID is within the valid range
    if not (0 <= selected_id < len(attractions_list)):
        raise ValueError(
            f"The selected ID '{selected_id}' is out of range. "
            "Ensure the AI response corresponds to a valid attraction in the list."
        )

    return attractions_list[selected_id]
