class FlightLoad:
    def __init__(
        self,
        flight_id: str,
        loaded_first_class: int,
        loaded_business_class: int,
        loaded_premium_economy_class: int,
        loaded_economy_class: int,
    ) -> None:
        self.flight_id = flight_id
        self.loaded_first_class = loaded_first_class
        self.loaded_business_class = loaded_business_class
        self.loaded_premium_economy_class = loaded_premium_economy_class
        self.loaded_economy_class = loaded_economy_class

    def to_dict(self) -> dict:
        return {
            "flightId": self.flight_id,
            "loadedKits": {
                "first": self.loaded_first_class,
                "business": self.loaded_business_class,
                "premiumEconomy": self.loaded_premium_economy_class,
                "economy": self.loaded_economy_class,
            },
        }

    def __repr__(self):
        return f"FlightLoad(\n flight_id={self.flight_id},\n loaded_first_class={self.loaded_first_class},\n loaded_business_class={self.loaded_business_class},\n loaded_premium_economy_class={self.loaded_premium_economy_class},\n loaded_economy_class={self.loaded_economy_class}\n)"

    def __str__(self):
        return self.__repr__()
