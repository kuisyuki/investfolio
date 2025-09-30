from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.auth import User


class UserRepository(ABC):
    """ユーザーリポジトリのインターフェース"""

    @abstractmethod
    async def create(self, user: User) -> User:
        """ユーザーを作成"""
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """IDでユーザーを取得"""
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        """ユーザー名でユーザーを取得"""
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """メールアドレスでユーザーを取得"""
        pass

    @abstractmethod
    async def exists_by_username(self, username: str) -> bool:
        """ユーザー名が存在するか確認"""
        pass

    @abstractmethod
    async def exists_by_email(self, email: str) -> bool:
        """メールアドレスが存在するか確認"""
        pass
