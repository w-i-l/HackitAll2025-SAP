from game_models.class_dict import ClassDict
from game_models.pending_kit import PendingKit
from game_models.kit_type import KitType, ALL_KIT_TYPES

class Airport:
    def __init__(
        self,
        code: str,
        storage_capacity: ClassDict,
        loading_kits_cost: ClassDict,
        processing_kits_cost: ClassDict,
        processing_kits_time_hours: ClassDict,
        current_kit_stock: ClassDict,
    ):
        
        self.code = code
        self.storage_capacity = storage_capacity
        self.loading_kits_cost = loading_kits_cost
        self.processing_kits_cost = processing_kits_cost
        self.processing_kits_time_hours = processing_kits_time_hours
        self.current_kit_stock = current_kit_stock
        self.kits_in_processing: list[PendingKit] = []
        
        
    def __repr__(self) -> str:
        return (
            f"Airport(code={self.code}, "
            f"storage_capacity={self.storage_capacity}, "
            f"loading_kits_cost={self.loading_kits_cost}, "
            f"processing_kits_cost={self.processing_kits_cost}, "
            f"processing_kits_time_hours={self.processing_kits_time_hours}, "
            f"current_kit_stock={self.current_kit_stock}, "
            f"kits_in_processing={self.kits_in_processing})"
        )
        
        
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Airport):
            return NotImplemented
        return (
            self.code == other.code and
            self.storage_capacity == other.storage_capacity and
            self.loading_kits_cost == other.loading_kits_cost and
            self.processing_kits_cost == other.processing_kits_cost and
            self.processing_kits_time_hours == other.processing_kits_time_hours and
            self.current_kit_stock == other.current_kit_stock and
            self.kits_in_processing == other.kits_in_processing
        )
        
        
    def copy(self) -> "Airport":
        copied_airport = Airport(
            code=self.code,
            storage_capacity=ClassDict(
                business_class=self.storage_capacity.business.amount,
                economy_class=self.storage_capacity.economy.amount,
                premium_economy_class=self.storage_capacity.premium_economy.amount,
                first_class=self.storage_capacity.first.amount,
            ),
            loading_kits_cost=ClassDict(
                business_class=self.loading_kits_cost.business.amount,
                economy_class=self.loading_kits_cost.economy.amount,
                premium_economy_class=self.loading_kits_cost.premium_economy.amount,
                first_class=self.loading_kits_cost.first.amount,
            ),
            processing_kits_cost=ClassDict(
                business_class=self.processing_kits_cost.business.amount,
                economy_class=self.processing_kits_cost.economy.amount,
                premium_economy_class=self.processing_kits_cost.premium_economy.amount,
                first_class=self.processing_kits_cost.first.amount,
            ),
            processing_kits_time_hours=ClassDict(
                business_class=self.processing_kits_time_hours.business.amount,
                economy_class=self.processing_kits_time_hours.economy.amount,
                premium_economy_class=self.processing_kits_time_hours.premium_economy.amount,
                first_class=self.processing_kits_time_hours.first.amount,
            ),
            current_kit_stock=ClassDict(
                business_class=self.current_kit_stock.business.amount,
                economy_class=self.current_kit_stock.economy.amount,
                premium_economy_class=self.current_kit_stock.premium_economy.amount,
                first_class=self.current_kit_stock.first.amount,
            ),
        )
        copied_airport.kits_in_processing = [kit.copy() for kit in self.kits_in_processing]
        return copied_airport
    
    
    def available_storage_capacity(self) -> ClassDict:
        return ClassDict(
            business_class=self.storage_capacity.business.amount - self.current_kit_stock.business.amount,
            economy_class=self.storage_capacity.economy.amount - self.current_kit_stock.economy.amount,
            premium_economy_class=self.storage_capacity.premium_economy.amount - self.current_kit_stock.premium_economy.amount,
            first_class=self.storage_capacity.first.amount - self.current_kit_stock.first.amount,
        )
        
        
    def can_store_kits(self, kits: ClassDict) -> bool:
        available_capacity = self.available_storage_capacity()
        return (
            kits.business.amount <= available_capacity.business.amount and
            kits.economy.amount <= available_capacity.economy.amount and
            kits.premium_economy.amount <= available_capacity.premium_economy.amount and
            kits.first.amount <= available_capacity.first.amount
        )
        
        
    def store_kits(self, kits: ClassDict) -> None:
        self.current_kit_stock = ClassDict(
            business_class=self.current_kit_stock.business.amount + kits.business.amount,
            economy_class=self.current_kit_stock.economy.amount + kits.economy.amount,
            premium_economy_class=self.current_kit_stock.premium_economy.amount + kits.premium_economy.amount,
            first_class=self.current_kit_stock.first.amount + kits.first.amount,
        )
        
        
    def remove_kits(self, kits: ClassDict) -> None:
        self.current_kit_stock = ClassDict(
            business_class=self.current_kit_stock.business.amount - kits.business.amount,
            economy_class=self.current_kit_stock.economy.amount - kits.economy.amount,
            premium_economy_class=self.current_kit_stock.premium_economy.amount - kits.premium_economy.amount,
            first_class=self.current_kit_stock.first.amount - kits.first.amount,
        )
        
        
    def add_kits_in_processing(self, pending_kit: PendingKit) -> None:
        self.kits_in_processing.append(pending_kit)
        
    
    def process_kits(self, at_day: int, at_hour: int) -> None:
        """
        !!! ONLY CALL THIS METHOD TO UPDATE KIT STOCKS !!!
        
        We keep the airports up to date by checking which kits have finished processing
        
        The day and hour should be the current day and hour in the game
        """
        remaining_kits_in_processing = []
        for pending_kit in self.kits_in_processing:
            for key_type in ALL_KIT_TYPES:
                kit_type_processing_hours = self.processing_kits_time_hours[key_type]
                
                available_hour = pending_kit.arrival_hour + kit_type_processing_hours
                available_day = pending_kit.arrival_day + (available_hour // 24)
                available_hour = available_hour % 24
                
                if (available_day < at_day) or (available_day == at_day and available_hour <= at_hour):
                    # Kits are ready to be added to current stock
                    self.current_kit_stock = ClassDict(
                        business_class=self.current_kit_stock.business.amount + (pending_kit.kits.business.amount if key_type == KitType.BUSINESS else 0),
                        economy_class=self.current_kit_stock.economy.amount + (pending_kit.kits.economy.amount if key_type == KitType.ECONOMY else 0),
                        premium_economy_class=self.current_kit_stock.premium_economy.amount + (pending_kit.kits.premium_economy.amount if key_type == KitType.PREMIUM_ECONOMY else 0),
                        first_class=self.current_kit_stock.first.amount + (pending_kit.kits.first.amount if key_type == KitType.FIRST else 0),
                    )
                    
                    pending_kit.kits = ClassDict(
                        business_class=pending_kit.kits.business.amount - (pending_kit.kits.business.amount if key_type == KitType.BUSINESS else 0),
                        economy_class=pending_kit.kits.economy.amount - (pending_kit.kits.economy.amount if key_type == KitType.ECONOMY else 0),
                        premium_economy_class=pending_kit.kits.premium_economy.amount - (pending_kit.kits.premium_economy.amount if key_type == KitType.PREMIUM_ECONOMY else 0),
                        first_class=pending_kit.kits.first.amount - (pending_kit.kits.first.amount if key_type == KitType.FIRST else 0),
                    )
                    
                if not pending_kit.kits.is_empty():
                    remaining_kits_in_processing.append(pending_kit)
                    
        self.kits_in_processing = remaining_kits_in_processing
    