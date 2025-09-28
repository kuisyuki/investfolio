from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class UserStock:
    """保有株エンティティ"""

    id: str
    user_id: str
    ticker_symbol: str
    quantity: int
    acquisition_price: float
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
