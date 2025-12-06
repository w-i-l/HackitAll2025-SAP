from enum import Enum
from typing import List

ALL_KIT_TYPES: List["KitType"] = [
    "BUSINESS",
    "ECONOMY",
    "PREMIUM_ECONOMY",
    "FIRST"
]

class KitType(Enum):
    BUSINESS = 0
    ECONOMY = 0
    PREMIUM_ECONOMY = 0
    FIRST = 0
    
    def __init__(self, amount: float = 0) -> None:
        self.amount = amount
        
        
    def __call__(self, amount: float = 0) -> "KitType":
        new_instance = self.__class__(self.value)
        new_instance.amount = amount
        return new_instance
    
    @property
    def weight(self) -> float:
        weights = {
            KitType.BUSINESS: 5,
            KitType.ECONOMY: 3,
            KitType.PREMIUM_ECONOMY: 2.5,
            KitType.FIRST: 1.5
        }
        return weights[self]
    
    @property
    def cost(self) -> int:
        costs = {
            KitType.BUSINESS: 200,
            KitType.ECONOMY: 150,
            KitType.PREMIUM_ECONOMY: 100,
            KitType.FIRST: 50
        }
        return costs[self]
    
    @property
    def order_lead_hours(self) -> int:
        lead_hours = {
            KitType.BUSINESS: 48,
            KitType.ECONOMY: 36,
            KitType.PREMIUM_ECONOMY: 24,
            KitType.FIRST: 12
        }
        return lead_hours[self]