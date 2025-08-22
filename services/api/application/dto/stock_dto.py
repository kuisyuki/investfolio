from pydantic import BaseModel
from datetime import datetime

class StockPriceResponse(BaseModel):
    symbol: str
    name: str
    price: float
    currency: str
    timestamp: datetime
    message: str