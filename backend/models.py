# backend/models.py
from dataclasses import dataclass

@dataclass
class Signal:
    symbol: str
    timeframe: str
    direction: str  # BUY / SELL / REVERSAL
    entry: float
    stop_loss: float
    confidence: str
    structure: str
    candle_close: str
