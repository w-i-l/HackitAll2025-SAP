from server_api_models.round_update import RoundUpdate

from game.game_state import GameState

class Agent:
    def __init__(self, name: str):
        self.name = name
        
        
    def __repr__(self) -> str:
        return f"Agent(name={self.name})"
    
    
    def decide(self, game_state: GameState) -> RoundUpdate:
        raise NotImplementedError("This method should be implemented by subclasses.")
    
    
    def on_round_end(
        self,
        game_state: GameState
    ) -> None:
        pass
    
    
    def on_game_end(
        self,
        game_state: GameState
    ) -> None:
        pass