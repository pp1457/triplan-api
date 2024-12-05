from typing import List, Optional, Union, Tuple
from datetime import date


class DateRange:
    """Represents the start and end dates of a trip."""
    def __init__(self, start: date, end: date):
        self.start = start
        self.end = end

    def __repr__(self):
        return f"DateRange(start={self.start}, end={self.end})"

class Location:
    """Represents a geographic location with latitude and longitude."""
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f"Location(latitude={self.latitude}, longitude={self.longitude})"

class Attraction:
    """Represents an attraction in the travel plan."""
    def __init__(
        self,
        name: str,
        address: str,
        description: Optional[str] = None,
        visit_duration: int = 0,
        travel_time_to_prev: int = 0,
        travel_time_to_next: int = 0,
        reviews: Optional[List[str]] = None,
        rating: Optional[float] = None,
        rating_count: Optional[int] = 0,
        ticket_price: Optional[float] = None,
        tags: Optional[List[str]] = None,
        url: Optional[str] = "",
        location: Optional[Location] = None
    ):
        self.type = "attraction"
        self.name = name
        self.address = address
        self.description = description
        self.visit_duration = visit_duration
        self.travel_time_to_prev = travel_time_to_prev
        self.travel_time_to_next = travel_time_to_next
        self.reviews = reviews
        self.rating = rating
        self.rating_count = rating_count
        self.ticket_price = ticket_price
        self.tags = tags or []
        self.url = url or ""
        self.location = location

    def __repr__(self):
        return (
            f"Attraction(type='{self.type}', name='{self.name}', address='{self.address}', "
            f"description='{self.description}', visit_duration={self.visit_duration}, "
            f"travel_time_to_prev={self.travel_time_to_prev}, travel_time_to_next={self.travel_time_to_next}, "
            f"reviews={self.reviews}, rating={self.rating}, rating_count={self.rating_count}, "
            f"ticket_price={self.ticket_price}, tags={self.tags}, url='{self.url}', "
            f"location={self.location})"
        )
class Travel:
    """Represents a travel segment in the travel plan."""
    def __init__(self, travel_mode: str, from_location: str, to_location: str, time: int, notes: Optional[str] = None):
        self.type = "travel"
        self.travel_mode = travel_mode
        self.from_location = from_location
        self.to_location = to_location
        self.time = time
        self.notes = notes

    def __repr__(self):
        return (f"Travel(type='{self.type}', travel_mode='{self.travel_mode}', from='{self.from_location}', "
                f"to='{self.to_location}', time={self.time}, notes='{self.notes}')")


class Trip:
    """Represents the entire trip."""
    def __init__(
        self,
        title: str,
        description: str,
        range: DateRange,
        travel_plan: List[Union[Attraction, Travel]],
    ):
        self.title = title
        self.description = description
        self.range = range
        self.travel_plan = travel_plan

    def __repr__(self):
        return (f"Trip(title='{self.title}', description='{self.description}', range={self.range}, "
                f"travel_plan={self.travel_plan})")
