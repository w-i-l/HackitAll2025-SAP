from typing import *

from game_models.kit_type import KitType

class ClassDict:
    def __init__(
        self,
        business_class: float,
        economy_class: float,
        premium_economy_class: float,
        first_class: float,
    ) -> None:
        self.business = KitType.BUSINESS(amount=business_class)
        self.economy = KitType.ECONOMY(amount=economy_class)
        self.premium_economy = KitType.PREMIUM_ECONOMY(amount=premium_economy_class)
        self.first = KitType.FIRST(amount=first_class)

    
    def __getitem__(self, key: KitType) -> float:
        if key == KitType.BUSINESS:
            return self.business.amount
        elif key == KitType.ECONOMY:
            return self.economy.amount
        elif key == KitType.PREMIUM_ECONOMY:
            return self.premium_economy.amount
        elif key == KitType.FIRST:
            return self.first.amount
        else:
            raise KeyError(f"Invalid KitType: {key}")
    
    def to_dict(self) -> Dict[str, float]:
        return {
            "business": self.business.amount,
            "economy": self.economy.amount,
            "premiumEconomy": self.premium_economy.amount,
            "first": self.first.amount,
        }
        
        
    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> "ClassDict":
        return cls(
            business_class=data.get("business", 0),
            economy_class=data.get("economy", 0),
            premium_economy_class=data.get("premiumEconomy", 0),
            first_class=data.get("first", 0),
        )
        
    
    def __repr__(self) -> str:
        return (
            f"ClassDict(business={self.business.amount}, "
            f"economy={self.economy.amount}, "
            f"premium_economy={self.premium_economy.amount}, "
            f"first={self.first.amount})"
        )
        
        
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ClassDict):
            return NotImplemented
        return (
            self.business.amount == other.business.amount and
            self.economy.amount == other.economy.amount and
            self.premium_economy.amount == other.premium_economy.amount and
            self.first.amount == other.first.amount
        )
        
        
    def total(self) -> float:
        return self.business.amount + self.economy.amount + self.premium_economy.amount + self.first.amount
    
    
    def is_empty(self) -> bool:
        return self.total() == 0
    
    
    def copy(self) -> "ClassDict":
        return ClassDict(
            business_class=self.business.amount,
            economy_class=self.economy.amount,
            premium_economy_class=self.premium_economy.amount,
            first_class=self.first.amount,
        )
        
        
    def add(self, other: "ClassDict") -> "ClassDict":
        return ClassDict(
            business_class=self.business.amount + other.business.amount,
            economy_class=self.economy.amount + other.economy.amount,
            premium_economy_class=self.premium_economy.amount + other.premium_economy.amount,
            first_class=self.first.amount + other.first.amount,
        )