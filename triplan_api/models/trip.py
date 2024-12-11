from typing import List, Optional, Union
from datetime import date, time
from enum import Enum
from pydantic import BaseModel

# Pydantic model for DateRange
class DateRange(BaseModel):
    """Represents the start and end dates of a trip."""
    start: date
    end: date

    def __repr__(self):
        return f"DateRange(start={self.start}, end={self.end})"

# Pydantic model for Location
class Location(BaseModel):
    """Represents a geographic location with latitude and longitude."""
    latitude: float
    longitude: float

    def __repr__(self):
        return f"Location(latitude={self.latitude}, longitude={self.longitude})"

class TimeSlot(str, Enum):
    MORNING = "morning"
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    AFTERNOON = "afternoon"
    DINNER = "dinner"
    NIGHT = "night"

# Pydantic model for Attraction
class Attraction(BaseModel):
    """Represents an attraction in the travel plan."""
    name: str
    address: Optional[str]
    place_id: Optional[str]
    time_slot: Optional[TimeSlot] = None
    description: Optional[str] = None
    visit_duration: int = 0
    travel_time_to_prev: int = 0
    travel_time_to_next: int = 0
    estimate_start_time: time
    estimate_end_time: time
    reviews: Optional[List[str]] = None
    rating: Optional[float] = None
    rating_count: Optional[int] = 0
    price_level: Optional[str] = None
    tags: Optional[List[str]] = None
    url: Optional[str] = ""
    location: Optional[Location] = None

    def __repr__(self):
        return (
            f"Attraction(type='attraction', name='{self.name}', address='{self.address}', "
            f"place_id='{self.place_id}', description='{self.description}', visit_duration={self.visit_duration}, "
            f"travel_time_to_prev={self.travel_time_to_prev}, travel_time_to_next={self.travel_time_to_next}, "
            f"estimate_start_time={self.estimate_start_time}, estimate_end_time={self.estimate_end_time}, "
            f"reviews={self.reviews}, rating={self.rating}, rating_count={self.rating_count}, "
            f"ticket_price={self.price_level}, tags={self.tags}, url='{self.url}', "
            f"location={self.location})"
        )

# Pydantic model for Travel
class Travel(BaseModel):
    """Represents a travel segment in the travel plan."""
    travel_mode: str
    from_location: str
    to_location: str
    time: int
    notes: Optional[str] = None

    def __repr__(self):
        return (f"Travel(type='travel', travel_mode='{self.travel_mode}', from='{self.from_location}', "
                f"to='{self.to_location}', time={self.time}, notes='{self.notes}')")

# Pydantic model for EmptySpot
class EmptySpot(BaseModel):
    """Represents an empty spot in the travel plan."""
    time_slot: TimeSlot
    estimate_start_time: time
    estimate_end_time: time

    def __repr__(self):
        return (f"EmptySpot(type='empty_spot', estimate_start_time={self.estimate_start_time}, "
                f"estimate_end_time={self.estimate_end_time}, time_slot='{self.time_slot}')")

# Updated Trip class to include EmptySpot in the travel_plan
class Trip(BaseModel):
    """Represents the entire trip."""
    title: str
    description: str
    range: DateRange
    travel_plan: List[Union[Attraction, Travel, EmptySpot]]

    def __repr__(self):
        return (f"Trip(title='{self.title}', description='{self.description}', range={self.range}, "
                f"travel_plan={self.travel_plan})")
