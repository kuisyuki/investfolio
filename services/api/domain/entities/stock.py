from dataclasses import dataclass
from datetime import datetime


@dataclass
class Stock:
    symbol: str
    name: str
    price: float
    currency: str
    timestamp: datetime
