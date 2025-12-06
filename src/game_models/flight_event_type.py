from enum import Enum

class FlightEventType(Enum):
    SCHEDULED = "SCEHEDULED"
    CHECKED_IN = "CHECKED_IN"
    LANDED = "LANDED"
    
    
    def __str__(self) -> str:
        return self.value
    
    
    def __repr__(self) -> str:
        return f"FlightEventType.{self.name}"
    
    
    @staticmethod
    def from_str(label: str) -> "FlightEventType":
        if label == "SCEHEDULED":
            return FlightEventType.SCHEDULED
        elif label == "CHECKED_IN":
            return FlightEventType.CHECKED_IN
        elif label == "LANDED":
            return FlightEventType.LANDED
        else:
            raise ValueError(f"Unknown FlightEventType: {label}")
