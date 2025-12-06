from server_api_models.flight_update import FlightUpdate
from server_api_models.penalty import Penalty


class StateUpdate:
    def __init__(
        self,
        day: int,
        hour: int,
        penalties: list[Penalty],
        flight_updates: list[FlightUpdate],
        total_cost: float,
    ) -> None:
        self.day = day
        self.hour = hour
        self.penalties = penalties
        self.flight_updates = flight_updates
        self.total_cost = total_cost

    def __repr__(self):
        return f"StateUpdate(\n day={self.day},\n hour={self.hour},\n penalties=[{len(self.penalties)} penalties],\n flight_updates=[{len(self.flight_updates)} flights updates],\n total_cost={self.total_cost:,.2f}\n)"

    def __str__(self):
        return self.__repr__()
