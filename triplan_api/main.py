from typing import Union, List

from fastapi import FastAPI
from pydantic import BaseModel

from triplan_api.core.gen import gen

app = FastAPI()

class TripRequest(BaseModel):
    trip: List[str]
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
    trip = gen(trip_request.trip, trip_request.user_input)
    return {"generated_trip": trip}
