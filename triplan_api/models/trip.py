from typing import List, Optional, Union
from datetime import date
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


# Pydantic model for Attraction
class Attraction(BaseModel):
    """Represents an attraction in the travel plan."""
    name: str
    address: str
    description: Optional[str] = None
    visit_duration: int = 0
    travel_time_to_prev: int = 0
    travel_time_to_next: int = 0
    reviews: Optional[List[str]] = None
    rating: Optional[float] = None
    rating_count: Optional[int] = 0
    ticket_price: Optional[float] = None
    tags: Optional[List[str]] = None
    url: Optional[str] = ""
    location: Optional[Location] = None

    def __repr__(self):
        return (
            f"Attraction(type='attraction', name='{self.name}', address='{self.address}', "
            f"description='{self.description}', visit_duration={self.visit_duration}, "
            f"travel_time_to_prev={self.travel_time_to_prev}, travel_time_to_next={self.travel_time_to_next}, "
            f"reviews={self.reviews}, rating={self.rating}, rating_count={self.rating_count}, "
            f"ticket_price={self.ticket_price}, tags={self.tags}, url='{self.url}', "
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


# Pydantic model for Trip
class Trip(BaseModel):
    """Represents the entire trip."""
    title: str
    description: str
    range: DateRange
    travel_plan: List[Union[Attraction, Travel]]

    def __repr__(self):
        return (f"Trip(title='{self.title}', description='{self.description}', range={self.range}, "
                f"travel_plan={self.travel_plan})")
