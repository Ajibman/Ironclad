from abc import ABC, abstractmethod
import datetime

class StrategyBase(ABC):
    def __init__(self, name: str, symbol: str):
        self.name = name
        self.symbol = symbol
        self.is_active = False

    @abstractmethod
    def on_tick(self, timestamp: datetime.datetime, price: float, quantity: float, is_buyer_maker: bool):
        """
        Executed immediately whenever the C++ ingestion layer pops 
        a clean WebSocket message frame and passes it down.
        """
        pass

    @abstractmethod
    def generate_signal(self) -> dict:
        """Calculates quantitative risk indicators to return trade commands."""
        pass
      
