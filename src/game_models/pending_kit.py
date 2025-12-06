from game_models.class_dict import ClassDict
from game_models.kit_type import KitType, ALL_KIT_TYPES

class PendingKit:
    def __init__(
        self,
        kits: ClassDict,
        arrival_day: int,    
        arrival_hour: int,
    ):
        self.kits = kits
        self.arrival_day = arrival_day
        self.arrival_hour = arrival_hour
        
        
    def __repr__(self) -> str:
        return (
            f"PendingKit(kits={self.kits}, "
            f"arrival_day={self.arrival_day}, "
            f"arrival_hour={self.arrival_hour})"
        )
        
        
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PendingKit):
            return NotImplemented
        return (
            self.kits == other.kits and
            self.arrival_day == other.arrival_day and
            self.arrival_hour == other.arrival_hour
        )
        
        
    def copy(self) -> "PendingKit":
        return PendingKit(
            kits=ClassDict(
                business_class=self.kits.business.amount,
                economy_class=self.kits.economy.amount,
                premium_economy_class=self.kits.premium_economy.amount,
                first_class=self.kits.first.amount,
            ),
            arrival_day=self.arrival_day,
            arrival_hour=self.arrival_hour,
        )
        
    
    def get_available_kits(
        self,
        at_day: int,
        at_hour: int,
        processing_lead_hours: ClassDict
    ) -> ClassDict:
        result = ClassDict()
        
        for kit_type in ALL_KIT_TYPES:
            kit_type_processing_hours = processing_lead_hours[kit_type]
            
            available_hour = self.arrival_hour + kit_type_processing_hours
            available_day = self.arrival_day + (available_hour // 24)
            available_hour = available_hour % 24
            
            if (at_day > available_day) or (at_day == available_day and at_hour >= available_hour):
                result[kit_type] = self.kits[kit_type]
            else:
                result[kit_type] = 0
                
        return result