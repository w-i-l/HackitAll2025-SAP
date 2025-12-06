from server_api_models.flight_load import FlightLoad
from server_api_models.kit_purchasing_order import KitPurchasingOrder


class RoundUpdate:
    def __init__(
        self,
        day: int,
        hour: int,
        flight_loads: list[FlightLoad],
        kit_purchasing_order: KitPurchasingOrder,
    ) -> None:
        self.day = day
        self.hour = hour
        self.flight_loads = flight_loads
        self.kit_purchasing_order = kit_purchasing_order or KitPurchasingOrder.empty()

    def to_dict(self) -> dict:
        return {
            "day": self.day,
            "hour": self.hour,
            "flightLoads": [flight_load.to_dict() for flight_load in self.flight_loads],
            "kitPurchasingOrders": self.kit_purchasing_order.to_dict(),
        }

    def __repr__(self):
        return f"RoundUpdates(\n day={self.day},\n hour={self.hour},\n flight_loads=[{len(self.flight_loads)} flight loads],\n kit_purchasing_order={self.kit_purchasing_order}\n)"

    def __str__(self):
        return self.__repr__()
