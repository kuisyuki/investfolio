from abc import ABC, abstractmethod

from domain.entities.user_stock import UserStock


class UserStockRepository(ABC):
    """保有株リポジトリのインターフェース"""

    @abstractmethod
    async def create(self, user_stock: UserStock) -> UserStock:
        """保有株を作成する"""
        raise NotImplementedError
