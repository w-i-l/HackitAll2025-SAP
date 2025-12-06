from game.agent import Agent

from game.game_state import GameState
from game.game_manager import GameManager

from server_api_models.round_update import RoundUpdate
from server_api_models.kit_purchasing_order import KitPurchasingOrder

class PassthroughAgent(Agent):
    def decide(self, game_state: GameState) -> RoundUpdate:
        return RoundUpdate(
            day=game_state.current_day,
            hour=game_state.current_hour,
            flight_loads=[],
            kit_purchasing_order=KitPurchasingOrder(
                first_class=0,
                business_class=0,
                premium_economy_class=0,
                economy_class=0,
            )
        )
        
        
def main():
    agent = PassthroughAgent(name="Passthrough Agent")
    
    game_manager = GameManager(agent=agent)
    
    game_manager.start_game()
    
    game_manager.play_game()
    
    game_manager.end_game()
    
if __name__ == "__main__":
    main()