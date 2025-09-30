import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreateRequest(BaseModel):
    """ユーザー作成リクエストスキーマ"""

    username: str = Field(default="guest_user", min_length=3, max_length=50)
    email: EmailStr = Field(default="user@example.com")
    password: str = Field(default="DefaultPass123", min_length=8, max_length=100)
    full_name: Optional[str] = Field(default="Guest User", max_length=100)

    @field_validator("username")
    def validate_username(cls, v):
        if not re.match(r"^[a-zA-Z0-9_-]+$", v):
            raise ValueError(
                "Username must contain only letters, numbers, hyphens and underscores"
            )
        return v

    @field_validator("password")
    def validate_password(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserResponse(BaseModel):
    """ユーザーレスポンススキーマ"""

    id: int
    user_id: int
    username: str
    email: str
    full_name: Optional[str]
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    """ログインリクエストスキーマ"""

    email: EmailStr = Field(..., description="メールアドレス")
    password: str = Field(..., min_length=8, max_length=100, description="パスワード")


class LoginResponse(BaseModel):
    """ログインレスポンススキーマ"""

    access_token: str = Field(..., description="アクセストークン")
    token_type: str = Field(default="bearer", description="トークンタイプ")
    user: UserResponse = Field(..., description="ユーザー情報")
