from typing import Optional

from domain.entities.auth import User
from domain.repositories.user_repository import UserRepository
from infrastructure.models.user import UserModel
from sqlalchemy.orm import Session


class SQLUserRepository(UserRepository):
    """SQLAlchemyを使用したユーザーリポジトリの実装"""

    def __init__(self, db: Session):
        self.db = db

    async def create(self, user: User) -> User:
        """ユーザーを作成"""
        user_model = UserModel(
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
            full_name=user.full_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
        )

        self.db.add(user_model)
        self.db.commit()
        self.db.refresh(user_model)

        # user_idにidと同じ値を設定
        user_model.user_id = user_model.id
        self.db.commit()
        self.db.refresh(user_model)

        return self._model_to_entity(user_model)

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """IDでユーザーを取得"""
        user_model = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        return self._model_to_entity(user_model) if user_model else None

    async def get_by_username(self, username: str) -> Optional[User]:
        """ユーザー名でユーザーを取得"""
        user_model = (
            self.db.query(UserModel).filter(UserModel.username == username).first()
        )
        return self._model_to_entity(user_model) if user_model else None

    async def get_by_email(self, email: str) -> Optional[User]:
        """メールアドレスでユーザーを取得"""
        user_model = self.db.query(UserModel).filter(UserModel.email == email).first()
        return self._model_to_entity(user_model) if user_model else None

    async def exists_by_username(self, username: str) -> bool:
        """ユーザー名が存在するか確認"""
        return (
            self.db.query(UserModel).filter(UserModel.username == username).first()
            is not None
        )

    async def exists_by_email(self, email: str) -> bool:
        """メールアドレスが存在するか確認"""
        return (
            self.db.query(UserModel).filter(UserModel.email == email).first()
            is not None
        )

    def _model_to_entity(self, model: UserModel) -> User:
        """モデルをエンティティに変換"""
        return User(
            id=model.id,
            username=model.username,
            email=model.email,
            password_hash=model.password_hash,
            user_id=model.user_id,
            full_name=model.full_name,
            is_active=model.is_active,
            is_verified=model.is_verified,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
