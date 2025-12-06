from typing import Set, Tuple

class FlightSchedule:
    def __init__(
        self,
        flight_number: str,
        origin_airport_id: str,
        destination_airport_id: str,
        departure_hour: int,
        arrival_hour: int,
        distance_km: float,
        frequency: Set[int],    
    ):
        self.flight_number = flight_number
        self.origin_airport_id = origin_airport_id
        self.destination_airport_id = destination_airport_id
        self.departure_hour = departure_hour
        self.arrival_hour = arrival_hour
        self.distance_km = distance_km
        self.frequency = frequency
        
        
    def __repr__(self) -> str:
        return (
            f"FlightSchedule(flight_number={self.flight_number}, "
            f"origin_airport_id={self.origin_airport_id}, "
            f"destination_airport_id={self.destination_airport_id}, "
            f"departure_hour={self.departure_hour}, "
            f"arrival_hour={self.arrival_hour}, "
            f"distance_km={self.distance_km}, "
            f"frequency={self.frequency})"
        )
        
        
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FlightSchedule):
            return NotImplemented
        return (
            self.flight_number == other.flight_number and
            self.origin_airport_id == other.origin_airport_id and
            self.destination_airport_id == other.destination_airport_id and
            self.departure_hour == other.departure_hour and
            self.arrival_hour == other.arrival_hour and
            self.distance_km == other.distance_km and
            self.frequency == other.frequency
        )
        
        
    def copy(self) -> "FlightSchedule":
        return FlightSchedule(
            flight_number=self.flight_number,
            origin_airport_id=self.origin_airport_id,
            destination_airport_id=self.destination_airport_id,
            departure_hour=self.departure_hour,
            arrival_hour=self.arrival_hour,
            distance_km=self.distance_km,
            frequency=set(self.frequency),
        )
        
        
    def operates_on_day(self, day: int) -> bool:
        normalised_day = day % 7
        return normalised_day in self.frequency
    
    
    def operates_on_date(self, at_day: int, at_hour: int) -> bool:
        flight_departure_day = at_day
        if at_hour < self.departure_hour:
            flight_departure_day -= 1
        return self.operates_on_day(flight_departure_day)
    
    
    def flight_duration_hours(self) -> int:
        if self.arrival_hour >= self.departure_hour:
            return self.arrival_hour - self.departure_hour
        else:
            return (24 - self.departure_hour) + self.arrival_hour
        
        
    def next_departure_after(self, current_day: int, current_hour: int) -> Tuple[int, int]:
        day = current_day
        hour = current_hour
        
        while True:
            if self.operates_on_date(day, hour):
                if hour <= self.departure_hour:
                    return (day, self.departure_hour)
            day += 1
            hour = 0
    