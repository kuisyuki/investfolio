from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from decimal import Decimal

class Portfolio(BaseModel):
    id: Optional[int] = None
    user_id: int
    name: str
    description: Optional[str] = None
    total_value: Decimal = Decimal("0.00")
    currency: str = "JPY"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PortfolioItem(BaseModel):
    id: Optional[int] = None
    portfolio_id: int
    symbol: str
    name: str
    quantity: Decimal
    average_price: Decimal
    current_price: Optional[Decimal] = None
    market_value: Optional[Decimal] = None
    gain_loss: Optional[Decimal] = None
    gain_loss_percent: Optional[float] = None
    asset_type: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True