from typing import List, Optional, Union
from datetime import date


class DateRange:
    """Represents the start and end dates of a trip."""
    def __init__(self, start: date, end: date):
        self.start = start
        self.end = end

    def __repr__(self):
        return f"DateRange(start={self.start}, end={self.end})"


class Attraction:
    """Represents an attraction in the travel plan."""
    def __init__(
        self,
        name: str,
        location: str,
        description: Optional[str] = None,
        visit_duration: int = 0,
        travel_time_to_prev: int = 0,
        travel_time_to_next: int = 0,
        review: Optional[str] = None,
        score: Optional[float] = None,
        ticket_price: Optional[float] = None,
        tags: Optional[List[str]] = None,
    ):
        self.type = "attraction"
        self.name = name
        self.location = location
        self.description = description
        self.visit_duration = visit_duration
        self.travel_time_to_prev = travel_time_to_prev
        self.travel_time_to_next = travel_time_to_next
        self.review = review
        self.score = score
        self.ticket_price = ticket_price
        self.tags = tags or []

    def __repr__(self):
        return (
            f"Attraction(type='{self.type}', name='{self.name}', location='{self.location}', "
            f"description='{self.description}', visit_duration={self.visit_duration}, "
            f"travel_time_to_prev={self.travel_time_to_prev}, travel_time_to_next={self.travel_time_to_next}, "
            f"review='{self.review}', score={self.score}, ticket_price={self.ticket_price}, tags={self.tags})"
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
