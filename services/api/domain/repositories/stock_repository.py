from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.stock import Stock


class StockRepository(ABC):
    @abstractmethod
    async def get_stock_price(self, symbol: str) -> Optional[Stock]:
        pass
