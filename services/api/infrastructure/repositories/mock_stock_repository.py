from datetime import datetime
from typing import Optional

from domain.entities.stock import Stock
from domain.repositories.stock_repository import StockRepository


class MockStockRepository(StockRepository):
    async def get_stock_price(self, symbol: str) -> Optional[Stock]:
        mock_prices = {
            "7974": Stock(
                symbol="7974",
                name="任天堂",
                price=8150.0,
                currency="JPY",
                timestamp=datetime.now(),
            )
        }
        return mock_prices.get(symbol)
