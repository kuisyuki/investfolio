"""ユーザーログインのユースケース"""

from typing import Optional

from domain.entities.auth import User
from domain.repositories.user_repository import UserRepository
from infrastructure.security import verify_password


class LoginUserUseCase:
    """ユーザーログインのユースケース"""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, email: str, password: str) -> Optional[User]:
        """
        メールアドレスとパスワードでユーザーをログイン

        Args:
            email: ログインメールアドレス
            password: ログインパスワード

        Returns:
            認証成功時はUserオブジェクト、失敗時はNone
        """
        # メールアドレスからユーザーを取得
        user = await self.user_repository.get_by_email(email)

        if not user:
            # ユーザーが存在しない
            return None

        # パスワードの検証
        if not verify_password(password, user.password_hash):
            # パスワードが一致しない
            return None

        # アカウントがアクティブか確認
        if not user.is_active:
            # アカウントが無効化されている
            return None

        return user