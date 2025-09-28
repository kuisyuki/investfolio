from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.sql import func

from infrastructure.database import Base


class UserStockModel(Base):
    __tablename__ = "user_stocks"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    ticker_symbol = Column(String(20), nullable=False)
    quantity = Column(Integer, nullable=False)
    acquisition_price = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
