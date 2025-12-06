from game_models.class_dict import ClassDict

class AircraftType:
    def __init__(
        self,
        name: str,
        passenger_capacity: ClassDict,
        kit_capacity: ClassDict,
        fuel_cost_per_km_per_kg: float,    
    ):
        self.name = name
        self.passenger_capacity = passenger_capacity
        self.kit_capacity = kit_capacity
        self.fuel_cost_per_km_per_kg = fuel_cost_per_km_per_kg
        
        
    def __repr__(self) -> str:
        return (
            f"AircraftType(name={self.name}, "
            f"passenger_capacity={self.passenger_capacity}, "
            f"kit_capacity={self.kit_capacity}, "
            f"fuel_cost_per_km_per_kg={self.fuel_cost_per_km_per_kg})"
        )
        
        
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AircraftType):
            return NotImplemented
        return (
            self.name == other.name and
            self.passenger_capacity == other.passenger_capacity and
            self.kit_capacity == other.kit_capacity and
            self.fuel_cost_per_km_per_kg == other.fuel_cost_per_km_per_kg
        )
        
        
    def copy(self) -> "AircraftType":
        return AircraftType(
            name=self.name,
            passenger_capacity=ClassDict(
                business_class=self.passenger_capacity.business.amount,
                economy_class=self.passenger_capacity.economy.amount,
                premium_economy_class=self.passenger_capacity.premium_economy.amount,
                first_class=self.passenger_capacity.first.amount,
            ),
            kit_capacity=ClassDict(
                business_class=self.kit_capacity.business.amount,
                economy_class=self.kit_capacity.economy.amount,
                premium_economy_class=self.kit_capacity.premium_economy.amount,
                first_class=self.kit_capacity.first.amount,
            ),
            fuel_cost_per_km_per_kg=self.fuel_cost_per_km_per_kg,
        )