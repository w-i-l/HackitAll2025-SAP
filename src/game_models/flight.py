from game_models.class_dict import ClassDict
from game_models.aircraft_type import AircraftType
from game_models.flight_event_type import FlightEventType



class Flight:
    def __init__(
        self,
        flight_id: str,
        flight_number: str,
        origin_airport_id: str,
        destination_airport_id: str,
        departure_day: int,
        departure_hour: int,
        arrival_day: int,
        arrival_hour: int,
        distance_km: float,
        aircraft_type: AircraftType,
        flight_event_type: FlightEventType,
        passager_count: ClassDict,
        loaded_kits: ClassDict,
    ):
        self.flight_id = flight_id
        self.flight_number = flight_number
        self.origin_airport_id = origin_airport_id
        self.destination_airport_id = destination_airport_id
        self.departure_day = departure_day
        self.departure_hour = departure_hour
        self.arrival_day = arrival_day
        self.arrival_hour = arrival_hour
        self.distance_km = distance_km
        self.aircraft_type = aircraft_type
        self.flight_event_type = flight_event_type
        self.passager_count = passager_count
        self.loaded_kits = loaded_kits
        
        
    def __repr__(self) -> str:
        return (
            f"Flight(flight_id={self.flight_id}, "
            f"flight_number={self.flight_number}, "
            f"origin_airport_id={self.origin_airport_id}, "
            f"destination_airport_id={self.destination_airport_id}, "
            f"departure_day={self.departure_day}, "
            f"departure_hour={self.departure_hour}, "
            f"arrival_day={self.arrival_day}, "
            f"arrival_hour={self.arrival_hour}, "
            f"distance_km={self.distance_km}, "
            f"aircraft_type={self.aircraft_type}, "
            f"flight_event_type={self.flight_event_type}, "
            f"passager_count={self.passager_count}, "
            f"loaded_kits={self.loaded_kits})"
        )
        
        
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Flight):
            return NotImplemented
        return (
            self.flight_id == other.flight_id and
            self.flight_number == other.flight_number and
            self.origin_airport_id == other.origin_airport_id and
            self.destination_airport_id == other.destination_airport_id and
            self.departure_day == other.departure_day and
            self.departure_hour == other.departure_hour and
            self.arrival_day == other.arrival_day and
            self.arrival_hour == other.arrival_hour and
            self.distance_km == other.distance_km and
            self.aircraft_type == other.aircraft_type and
            self.flight_event_type == other.flight_event_type and
            self.passager_count == other.passager_count and
            self.loaded_kits == other.loaded_kits
        )
        
        
    def copy(self) -> "Flight":
        return Flight(
            flight_id=self.flight_id,
            flight_number=self.flight_number,
            origin_airport_id=self.origin_airport_id,
            destination_airport_id=self.destination_airport_id,
            departure_day=self.departure_day,
            departure_hour=self.departure_hour,
            arrival_day=self.arrival_day,
            arrival_hour=self.arrival_hour,
            distance_km=self.distance_km,
            aircraft_type=self.aircraft_type.copy(),
            flight_event_type=self.flight_event_type,
            passager_count=ClassDict(
                business_class=self.passager_count.business.amount,
                economy_class=self.passager_count.economy.amount,
                premium_economy_class=self.passager_count.premium_economy.amount,
                first_class=self.passager_count.first.amount,
            ),
            loaded_kits=ClassDict(
                business_class=self.loaded_kits.business.amount,
                economy_class=self.loaded_kits.economy.amount,
                premium_economy_class=self.loaded_kits.premium_economy.amount,
                first_class=self.loaded_kits.first.amount,
            ),
        )