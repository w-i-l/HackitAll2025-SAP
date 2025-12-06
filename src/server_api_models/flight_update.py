# {
#       "eventType": "SCHEDULED",
#       "flightNumber": "string",
#       "flightId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#       "originAirport": "string",
#       "destinationAirport": "string",
#       "departure": {
#         "day": 0,
#         "hour": 0
#       },
#       "arrival": {
#         "day": 0,
#         "hour": 0
#       },
#       "passengers": {
#         "first": 42000,
#         "business": 42000,
#         "premiumEconomy": 1000,
#         "economy": 42000
#       },
#       "aircraftType": "string"
#     }


class FlightUpdate:
    def __init__(
        self,
        event_type: str,
        flight_number: str,
        flight_id: str,
        origin_airport: str,
        destination_airport: str,
        departure_day: int,
        departure_hour: int,
        arrival_day: int,
        arrival_hour: int,
        passengers_first: int,
        passengers_business: int,
        passengers_premium_economy: int,
        passengers_economy: int,
        aircraft_type: str,
        distance: int = 0,
    ) -> None:
        self.event_type = event_type
        self.flight_number = flight_number
        self.flight_id = flight_id
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.departure_day = departure_day
        self.departure_hour = departure_hour
        self.arrival_day = arrival_day
        self.arrival_hour = arrival_hour
        self.passengers_first = passengers_first
        self.passengers_business = passengers_business
        self.passengers_premium_economy = passengers_premium_economy
        self.passengers_economy = passengers_economy
        self.aircraft_type = aircraft_type
        self.distance = distance

    @classmethod
    def from_dict(cls, data: dict) -> "FlightUpdate":
        return cls(
            event_type=data.get("eventType"),
            flight_number=data.get("flightNumber"),
            flight_id=data.get("flightId"),
            origin_airport=data.get("originAirport"),
            destination_airport=data.get("destinationAirport"),
            departure_day=data.get("departure", {}).get("day"),
            departure_hour=data.get("departure", {}).get("hour"),
            arrival_day=data.get("arrival", {}).get("day"),
            arrival_hour=data.get("arrival", {}).get("hour"),
            passengers_first=data.get("passengers", {}).get("first"),
            passengers_business=data.get("passengers", {}).get("business"),
            passengers_premium_economy=data.get("passengers", {}).get("premiumEconomy"),
            passengers_economy=data.get("passengers", {}).get("economy"),
            aircraft_type=data.get("aircraftType"),
            distance=data.get("distance", 0),
        )

    def __repr__(self):
        return f"FlightUpdate(\n event_type={self.event_type},\n flight_number={self.flight_number},\n flight_id={self.flight_id},\n origin_airport={self.origin_airport},\n destination_airport={self.destination_airport},\n departure_day={self.departure_day},\n departure_hour={self.departure_hour},\n arrival_day={self.arrival_day},\n arrival_hour={self.arrival_hour},\n passengers_first={self.passengers_first},\n passengers_business={self.passengers_business},\n passengers_premium_economy={self.passengers_premium_economy},\n passengers_economy={self.passengers_economy},\n aircraft_type={self.aircraft_type},\n distance={self.distance}\n)"

    def __str__(self):
        return self.__repr__()
