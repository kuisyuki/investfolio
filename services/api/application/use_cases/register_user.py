from domain.entities.auth import User
from domain.repositories.user_repository import UserRepository
from infrastructure.security import hash_password


class RegisterUserUseCase:
    """ユーザー登録のユースケース"""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(
        self, username: str, email: str, password: str, full_name: str = None
    ) -> User:
        """ユーザーを登録"""

        # ユーザー名の重複チェック
        if await self.user_repository.exists_by_username(username):
            raise ValueError(f"Username '{username}' already exists")

        # メールアドレスの重複チェック
        if await self.user_repository.exists_by_email(email):
            raise ValueError(f"Email '{email}' already exists")

        # パスワードをハッシュ化
        password_hash = hash_password(password)

        # ユーザーエンティティを作成
        user = User(
            id="",  # リポジトリで生成される
            username=username,
            email=email,
            password_hash=password_hash,
            full_name=full_name,
            is_active=True,
            is_verified=False,
        )

        # ユーザーを保存
        created_user = await self.user_repository.create(user)

        return created_user
