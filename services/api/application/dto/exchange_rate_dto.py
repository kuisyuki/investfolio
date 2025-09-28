from pydantic import BaseModel
from typing import Optional

class ExchangeRateDTO(BaseModel):
    symbol: str
    ask: Optional[str] = None
    bid: Optional[str] = None
    high: Optional[str] = None
    low: Optional[str] = None
    last: Optional[str] = None
