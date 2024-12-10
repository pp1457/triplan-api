from typing import Union, List

from fastapi import FastAPI
from pydantic import BaseModel

from datetime import time

from triplan_api.core.gen import gen
from triplan_api.models.trip import *
from triplan_api.utils.process_user_input import *

app = FastAPI()

class TripRequest(BaseModel):
    trip: Trip
    user_input: str

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@app.post("/generate_trip")
def generate_trip(trip_request: TripRequest):
    """
    Endpoint to generate a trip.
    """
    #parsed_input = process_user_input(user_input)
    #trip = gen(trip_request.trip, trip_request.user_input)

    current_trip = [
        Attraction(
            name="Home",
            address="Starting Point",
            place_id="home_001",
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
            location=Location(latitude=40.7128, longitude=-74.0060)
        ),
        Travel(
            travel_mode="car",
            from_location="Home",
            to_location="Breakfast Place",
            time=30,
            notes="Travel to the breakfast spot."
        ),
        Attraction(
            name="Breakfast Spot",
            address="Local Diner",
            place_id="breakfast_001",
            time_slot=TimeSlot.BREAKFAST,
            visit_duration=60,
            travel_time_to_prev=30,
            travel_time_to_next=20,
            estimate_start_time=time(8, 30),
            estimate_end_time=time(9, 30),
            tags=["food", "breakfast"],
            description="Enjoy a delicious breakfast to start your day.",
            reviews=["Great pancakes!", "Friendly staff."],
            rating=4.2,
            rating_count=85,
            ticket_price=15.0,
            url="http://example.com/breakfast",
            location=Location(latitude=40.7138, longitude=-74.0050)
        ),
        Travel(
            travel_mode="walk",
            from_location="Breakfast Spot",
            to_location="Museum",
            time=20,
            notes="Walk to the museum."
        ),
        Attraction(
            name="Museum of Natural History",
            address="Museum Address",
            place_id="museum_001",
            time_slot=TimeSlot.AFTERNOON,
            visit_duration=120,
            travel_time_to_prev=20,
            travel_time_to_next=60,
            estimate_start_time=time(10, 0),
            estimate_end_time=time(12, 0),
            tags=["history", "learning"],
            description="Explore the wonders of natural history.",
            reviews=["Informative exhibits!", "Great for kids."],
            rating=4.8,
            rating_count=1200,
            ticket_price=25.0,
            url="http://example.com/museum",
            location=Location(latitude=40.7812, longitude=-73.9735)
        ),
        Travel(
            travel_mode="bus",
            from_location="Museum",
            to_location="Lunch Spot",
            time=30,
            notes="Travel to the lunch spot."
        ),
        Attraction(
            name="Lunch Spot",
            address="City Center Restaurant",
            place_id="lunch_001",
            time_slot=TimeSlot.LUNCH,
            visit_duration=90,
            travel_time_to_prev=30,
            travel_time_to_next=30,
            estimate_start_time=time(12, 30),
            estimate_end_time=time(14, 0),
            tags=["food", "lunch"],
            description="A relaxing lunch break at a cozy restaurant.",
            reviews=["Fantastic pasta!", "Quick service."],
            rating=4.3,
            rating_count=200,
            ticket_price=30.0,
            url="http://example.com/lunch",
            location=Location(latitude=40.7580, longitude=-73.9855)
        ),
        Travel(
            travel_mode="taxi",
            from_location="Lunch Spot",
            to_location="Hotel",
            time=30,
            notes="Return to the hotel."
        ),
        Attraction(
            name="Hotel",
            address="Destination",
            place_id="hotel_001",
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
            location=Location(latitude=48.8566, longitude=2.3522)
        )
    ]

    return {"generated_trip": trip}
