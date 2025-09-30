from abc import ABC, abstractmethod
from typing import List

from domain.entities.user_stock import UserStock


class UserStockRepository(ABC):
    """保有株リポジトリのインターフェース"""

    @abstractmethod
    async def create(self, user_stock: UserStock) -> UserStock:
        """保有株を作成する"""
        raise NotImplementedError

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> List[UserStock]:
        """ユーザーIDで保有株リストを取得する"""
        raise NotImplementedError
