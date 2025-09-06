from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """ユーザーエンティティ"""

    id: str
    username: str
    email: str
    password_hash: str
    full_name: Optional[str] = None
    is_active: bool = True
    is_verified: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
