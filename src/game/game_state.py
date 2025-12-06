from typing import Dict, List

from game_models.aircraft_type import AircraftType
from game_models.airport import Airport
from game_models.flight import Flight
from game_models.flight_event_type import FlightEventType
from game_models.class_dict import ClassDict
from game_models.pending_kit import PendingKit
from game_models.flight_scheduele import FlightSchedule
from game_models.kit_type import KitType, ALL_KIT_TYPES
from game.data_loader import DataLoader

from server_api_models.flight_update import FlightUpdate
from server_api_models.flight_load import FlightLoad
from server_api_models.kit_purchasing_order import KitPurchasingOrder


class GameState:
    def __init__(self):
        self.current_day: int = 0
        self.current_hour: int = 0
        self.current_round: int = 0
        
        self.airports: List[Airport] = []
        self.aircraft_types: List[AircraftType] = []
        self.hub_code: str = ""
        
        self.kits_in_delivery: List[PendingKit] = []
        self.data_loader = DataLoader()
        
        self.flights_schedueles: List[FlightSchedule] = []
        self.flights_by_id: Dict[str, Flight] = {}
        
        
    @property
    def flights(self) -> List[Flight]:
        return list(self.flights_by_id.values())   
        
        
    def load_data(self) -> None:
        self.aircraft_types = list(self.data_loader.load_aircraft_types().values())
        self.airports = list(self.data_loader.load_airports().values())
        self.flights_schedueles = list(self.data_loader.load_flight_schedules().values())
    
    
    def get_aircraft_type_by_name(self, name: str) -> AircraftType | None:
        for aircraft_type in self.aircraft_types:
            if aircraft_type.name == name:
                return aircraft_type
        return None
    
    
    def get_airport_by_code(self, code: str) -> Airport | None:
        for airport in self.airports:
            if airport.code == code:
                return airport
        return None
        
        
    def update_flights_from_api(self, flight_updates: List[FlightUpdate]) -> None:
        for flight_update in flight_updates:
            flight_id = flight_update.flight_id
            
            if flight_update.event_type == FlightEventType.SCHEDULED.value:
                new_flight = Flight(
                    flight_id=flight_id,
                    flight_number=flight_update.flight_number,
                    origin_airport_id=flight_update.origin_airport,
                    destination_airport_id=flight_update.destination_airport,
                    departure_day=flight_update.departure_day,
                    departure_hour=flight_update.departure_hour,
                    arrival_day=flight_update.arrival_day,
                    arrival_hour=flight_update.arrival_hour,
                    distance_km=flight_update.distance,
                    aircraft_type=self.get_aircraft_type_by_name(flight_update.aircraft_type),
                    flight_event_type=FlightEventType.SCHEDULED,
                    passager_count=ClassDict(
                        business_class=flight_update.passengers_business,
                        economy_class=flight_update.passengers_economy,
                        premium_economy_class=flight_update.passengers_premium_economy,
                        first_class=flight_update.passengers_first,
                    ),
                    loaded_kits=ClassDict(),
                )
                
                self.flights_by_id[flight_id] = new_flight
                
                
            else:  # UPDATE existing flight
                if flight_id in self.flights_by_id:
                    flight = self.flights_by_id[flight_id]
                    flight.passager_count = ClassDict(
                        business_class=flight_update.passengers_business,
                        economy_class=flight_update.passengers_economy,
                        premium_economy_class=flight_update.passengers_premium_economy,
                        first_class=flight_update.passengers_first,
                    )
                    flight.flight_event_type = FlightEventType.CHECKED_IN
                    flight.arrival_day = flight_update.arrival_day
                    flight.arrival_hour = flight_update.arrival_hour
                    flight.departure_day = flight_update.departure_day
                    flight.departure_hour = flight_update.departure_hour
                    flight.distance_km = flight_update.distance
                   
                   
    def update_hub(self, hub_orders: List[KitPurchasingOrder]) -> None:
        self.update_hub_new_orders(hub_orders)
        self.process_pending_kits_in_hub()
    
    
    def process_pending_kits_in_hub(self) -> None:
        hub_airport = self.get_airport_by_code(self.hub_code)
        if not hub_airport:
            return

        remaining_kits_in_delivery = []
        for pending_kit in self.kits_in_delivery:
            if (self.current_day > pending_kit.arrival_day) or \
               (self.current_day == pending_kit.arrival_day and self.current_hour >= pending_kit.arrival_hour):
                   for key_type in ALL_KIT_TYPES:
                       kit_type_processing_hours = key_type.order_lead_hours
                       
                       available_hour = pending_kit.arrival_hour + kit_type_processing_hours
                       available_day = pending_kit.arrival_day + (available_hour // 24)
                       available_hour = available_hour % 24
                       
                       hub_airport.store_kits(ClassDict(
                           business_class=pending_kit.kits.business.amount if key_type == KitType.BUSINESS else 0,
                           economy_class=pending_kit.kits.economy.amount if key_type == KitType.ECONOMY else 0,
                           premium_economy_class=pending_kit.kits.premium_economy.amount if key_type == KitType.PREMIUM_ECONOMY else 0,
                           first_class=pending_kit.kits.first.amount if key_type == KitType.FIRST else 0,
                       ))
                       
                       pending_kit.kits = ClassDict(
                           business_class=pending_kit.kits.business.amount - (pending_kit.kits.business.amount if key_type == KitType.BUSINESS else 0),
                           economy_class=pending_kit.kits.economy.amount - (pending_kit.kits.economy.amount if key_type == KitType.ECONOMY else 0),
                           premium_economy_class=pending_kit.kits.premium_economy.amount - (pending_kit.kits.premium_economy.amount if key_type == KitType.PREMIUM_ECONOMY else 0),
                           first_class=pending_kit.kits.first.amount - (pending_kit.kits.first.amount if key_type == KitType.FIRST else 0),
                       )
            else:
                remaining_kits_in_delivery.append(pending_kit)
                
        self.kits_in_delivery = remaining_kits_in_delivery
     
     
    def update_hub_new_orders(self, hub_orders: List[KitPurchasingOrder]) -> None:
        hub_airport = self.get_airport_by_code(self.hub_code)
        if not hub_airport:
            return

        for order in hub_orders:
            pending_kit = PendingKit(
                kits=ClassDict(
                    business_class=order.ordered_business_class,
                    economy_class=order.ordered_economy_class,
                    premium_economy_class=order.ordered_premium_economy_class,
                    first_class=order.ordered_first_class,
                ),
                arrival_day=self.current_day,
                arrival_hour=self.current_hour,
            )
            self.kits_in_delivery.append(pending_kit)
                    
                    
    def update_airports(
        self,
        flights_updates: List[FlightUpdate],
        flights_loads: List[FlightLoad]
    ) -> None:
        """
        !!! SHOULD BE CALLED AFTER update_flights_from_api AND IN THE CORRECT ORDER !!!
        """
        self.update_airports_kits_for_checked_in_flights(flights_updates, flights_loads)
        self.update_airports_kits_from_new_landed_flights(flights_updates)
        self.process_pending_kits_in_all_airports()
    
    
    def update_airports_kits_for_checked_in_flights(
        self,
        flights_updates: List[FlightUpdate],
        flights_loads: List[FlightLoad]
    ) -> None:
        """
        !!! SHOULD BE CALLED AFTER update_flights_from_api AND IN THE CORRECT ORDER !!!
        
        """
        
        for flight_update in flights_updates:
            if flight_update.event_type == FlightEventType.CHECKED_IN.value and\
                flight_update.departure_day == self.current_day and\
                    flight_update.departure_hour == self.current_hour:
                
                origin_airport = self.get_airport_by_code(flight_update.origin_airport)
                
                if origin_airport:
                    flight = self.flights_by_id.get(flight_update.flight_id)
                    flight_load = next(
                        (fl for fl in flights_loads if fl.flight_id == flight_update.flight_id),
                        None
                    )
                    if flight and flight_load:
                        origin_airport.remove_kits(flight.loaded_kits)
                        flight.loaded_kits = ClassDict(
                            business_class=flight_load.loaded_business_class,
                            economy_class=flight_load.loaded_economy_class,
                            premium_economy_class=flight_load.loaded_premium_economy_class,
                            first_class=flight_load.loaded_first_class,
                        )
    
    
    def update_airports_kits_from_new_landed_flights(self, flights_updates: List[FlightUpdate]) -> None:
        """
        !!! SHOULD BE CALLED AFTER update_flights_from_api AND IN THE CORRECT ORDER !!!
        
        """
        for flight_update in flights_updates:
            if flight_update.event_type == FlightEventType.LANDED.value and\
                flight_update.arrival_day == self.current_day and\
                    flight_update.arrival_hour == self.current_hour:
                destination_airport = self.get_airport_by_code(flight_update.destination_airport)
                
                if destination_airport:
                    flight = self.flights_by_id.get(flight_update.flight_id)
                    if flight:
                        destination_airport.add_kits_in_processing(
                            PendingKit(
                                kits=flight.loaded_kits.copy(),
                                arrival_day=flight.arrival_day,
                                arrival_hour=flight.arrival_hour,
                            )
                        )
                        
    
    def process_pending_kits_in_all_airports(self) -> None:
        """
        !!! SHOULD BE CALLED AFTER update_flights_from_api AND IN THE CORRECT ORDER !!!
        
        """
        for airport in self.airports:
            airport.process_kits(self.current_day, self.current_hour)

                        
    