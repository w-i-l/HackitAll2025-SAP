from typing import List, Dict

from game_models.aircraft_type import AircraftType
from game_models.airport import Airport
from game_models.flight import Flight
from game_models.flight_scheduele import FlightSchedule

from game.game_state import GameState
from game.agent import Agent

from api.client_api import ClientAPI


class GameManager:
    def __init__(
        self,
        agent: Agent,
        api_key: str = "7bcd6334-bc2e-4cbf-b9d4-61cb9e868869",
    ):
        self.game_state = GameState()
        self.agent = agent
        self.client_api = ClientAPI(api_key)
        self.total_rounds = 720
        self.max_days = 30
        self.max_hours_per_day = 24
        
    def start_game(self) -> None:
        session_response = self.client_api.start_session()
        
        if isinstance(session_response, Exception):
            print(f"Error starting session: {session_response}")
            return
        
        print(f"Session started with ID: {session_response}")       

        
    def play_game(self) -> None:
        for day in range(self.max_days):
            for hour in range(self.max_hours_per_day):
                print(f"Day {day}, Hour {hour} - Starting round")
                
                self.play_game_round(day, hour)
        
        self.agent.on_game_end(self.game_state)
            
            
    def play_game_round(self, day: int, hour: int) -> None:
        round_update = self.agent.decide(self.game_state)
        round_update.day = day
        round_update.hour = hour
        
        response = self.client_api.play_round(round_update)
        
        if isinstance(response, Exception):
            print(f"Error during round: {response}")
            return
        
        print(f"Received total penalty: {response.total_cost:,.2f}")
        
        self.game_state.update_airports(
            flights_updates=response.flight_updates,
            flights_loads=round_update.flight_loads
        )
        
        self.game_state.update_hub(hub_order=round_update.kit_purchasing_order)
        
        self.game_state.advance_time()
        
        self.agent.on_round_end(self.game_state)
        
    
    def end_game(self) -> None:
        response = self.client_api.stop_session()
        
        if isinstance(response, Exception):
            print(f"Error ending session: {response}")
            return
        
        print("Game ended successfully.")