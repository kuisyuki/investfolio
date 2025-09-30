"""認証関連の依存性注入"""

from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from domain.entities.auth import User
from infrastructure.database import get_db
from infrastructure.repositories.user_repository import SQLUserRepository
from infrastructure.jwt_utils import verify_token

# Bearer認証スキームの定義
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """
    現在認証されているユーザーを取得

    Args:
        credentials: Bearer認証のクレデンシャル
        db: データベースセッション

    Returns:
        認証されたユーザーオブジェクト

    Raises:
        HTTPException: トークンが無効な場合
    """
    token = credentials.credentials

    # トークンを検証
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # トークンからユーザーIDを取得
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # データベースからユーザーを取得
    user_repository = SQLUserRepository(db)
    user = await user_repository.get_by_id(int(user_id))

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        HTTPBearer(auto_error=False)
    ),
    db: Session = Depends(get_db),
) -> Optional[User]:
    """
    オプショナルな認証（認証がなくてもアクセス可能）

    Args:
        credentials: Bearer認証のクレデンシャル（オプショナル）
        db: データベースセッション

    Returns:
        認証されたユーザーオブジェクト、または認証されていない場合はNone
    """
    if not credentials:
        return None

    try:
        return await get_current_user(credentials, db)
    except HTTPException:
        return None