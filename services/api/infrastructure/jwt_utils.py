"""JWT token management utilities"""

import os
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt

# 環境変数から設定を取得（開発環境用デフォルト値付き）
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    JWTアクセストークンを生成

    Args:
        data: トークンに含めるデータ
        expires_delta: トークンの有効期限（指定しない場合はデフォルト値を使用）

    Returns:
        生成されたJWTトークン
    """
    to_encode = data.copy()

    # 有効期限の設定
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    # JWTトークンの生成
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """
    JWTトークンを検証してデコード

    Args:
        token: 検証するJWTトークン

    Returns:
        デコードされたトークンのペイロード。無効な場合はNone
    """
    try:
        # トークンをデコード
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def get_user_id_from_token(token: str) -> Optional[str]:
    """
    トークンからユーザーIDを取得

    Args:
        token: JWTトークン

    Returns:
        ユーザーID。取得できない場合はNone
    """
    payload = verify_token(token)
    if payload:
        return payload.get("sub")
    return None