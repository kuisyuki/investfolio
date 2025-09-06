from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class TransactionType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    DIVIDEND = "DIVIDEND"
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"


class Transaction(BaseModel):
    id: Optional[int] = None
    user_id: int
    portfolio_id: int
    symbol: str
    transaction_type: TransactionType
    quantity: Decimal
    price: Decimal
    total_amount: Decimal
    fee: Decimal = Decimal("0.00")
    tax: Decimal = Decimal("0.00")
    currency: str = "JPY"
    transaction_date: datetime
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
