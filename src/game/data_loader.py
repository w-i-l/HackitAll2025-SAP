import pandas as pd
from typing import Dict, List
import os
from game_models.aircraft_type import AircraftType
from game_models.airport import Airport
from game_models.class_dict import ClassDict
from game_models.flight_scheduele import FlightSchedule
from game_models.flight_event_type import FlightEventType

DEFAULT_DATA_PATH = "../eval-platform/src/main/resources/liquibase/data/"


class DataLoader:
    def __init__(self):
        pass

    def load_aircraft_types(
        self, csv_path: str = "aircraft_types.csv"
    ) -> Dict[str, AircraftType]:
        """
        Loads aircraft types from a CSV file.
        Returns a dictionary mapping aircraft ID (UUID) to AircraftType objects.
        """
        csv_path = os.path.join(DEFAULT_DATA_PATH, csv_path)
        df = pd.read_csv(csv_path, sep=";")
        aircraft_types = {}

        for _, row in df.iterrows():
            passenger_capacity = ClassDict(
                business_class=row["business_seats"],
                economy_class=row["economy_seats"],
                premium_economy_class=row["premium_economy_seats"],
                first_class=row["first_class_seats"],
            )

            kit_capacity = ClassDict(
                business_class=row["business_kits_capacity"],
                economy_class=row["economy_kits_capacity"],
                premium_economy_class=row["premium_economy_kits_capacity"],
                first_class=row["first_class_kits_capacity"],
            )

            aircraft = AircraftType(
                name=row["type_code"],
                passenger_capacity=passenger_capacity,
                kit_capacity=kit_capacity,
                fuel_cost_per_km_per_kg=row["cost_per_kg_per_km"],
            )

            aircraft_types[row["id"]] = aircraft

        return aircraft_types

    def load_airports(
        self, csv_path: str = "airports_with_stocks.csv"
    ) -> Dict[str, Airport]:
        """
        Loads airports from a CSV file.
        Returns a dictionary mapping airport ID (UUID) to Airport objects.
        """
        csv_path = os.path.join(DEFAULT_DATA_PATH, csv_path)

        df = pd.read_csv(csv_path, sep=";")
        airports = {}

        for _, row in df.iterrows():
            storage_capacity = ClassDict(
                business_class=row.get("capacity_bc", 0),
                economy_class=row.get("capacity_ec", 0),
                premium_economy_class=row.get("capacity_pe", 0),
                first_class=row.get("capacity_fc", 0),
            )

            loading_kits_cost = ClassDict(
                business_class=row["business_loading_cost"],
                economy_class=row["economy_loading_cost"],
                premium_economy_class=row["premium_economy_loading_cost"],
                first_class=row["first_loading_cost"],
            )

            processing_kits_cost = ClassDict(
                business_class=row["business_processing_cost"],
                economy_class=row["economy_processing_cost"],
                premium_economy_class=row["premium_economy_processing_cost"],
                first_class=row["first_processing_cost"],
            )

            processing_kits_time_hours = ClassDict(
                business_class=row["business_processing_time"],
                economy_class=row["economy_processing_time"],
                premium_economy_class=row["premium_economy_processing_time"],
                first_class=row["first_processing_time"],
            )

            current_kit_stock = ClassDict(
                business_class=row.get("initial_bc_stock", 0),
                economy_class=row.get("initial_ec_stock", 0),
                premium_economy_class=row.get("initial_pe_stock", 0),
                first_class=row.get("initial_fc_stock", 0),
            )

            airport = Airport(
                code=row["code"],
                storage_capacity=storage_capacity,
                loading_kits_cost=loading_kits_cost,
                processing_kits_cost=processing_kits_cost,
                processing_kits_time_hours=processing_kits_time_hours,
                current_kit_stock=current_kit_stock,
            )

            airports[row["id"]] = airport

        return airports

    def load_flight_schedules(
        self, csv_path: str = "flight_plan.csv"
    ) -> List[FlightSchedule]:
        """
        Loads flight schedules from a CSV file (flight_plan.csv).
        """

        csv_path = os.path.join(DEFAULT_DATA_PATH, csv_path)
        df = pd.read_csv(csv_path, sep=";")
        schedules = []

        # Mapping CSV day columns to integers (Mon=0, Sun=6)
        days_mapping = {
            "Mon": 0,
            "Tue": 1,
            "Wed": 2,
            "Thu": 3,
            "Fri": 4,
            "Sat": 5,
            "Sun": 6,
        }

        for _, row in df.iterrows():
            frequency: Set[int] = set()
            for day_col, day_int in days_mapping.items():
                if row[day_col] == 1:
                    frequency.add(day_int)

            # Since flight_number is missing in the CSV, we generate a unique ID
            generated_flight_number = (
                f"{row['depart_code']}_{row['arrival_code']}_{row['scheduled_hour']}"
            )

            schedule = FlightSchedule(
                flight_number=generated_flight_number,
                origin_airport_id=row["depart_code"],
                destination_airport_id=row["arrival_code"],
                departure_hour=row["scheduled_hour"],
                arrival_hour=row["scheduled_arrival_hour"],
                distance_km=row["distance_km"],
                frequency=frequency,
            )
            schedules.append(schedule)

        return schedules
