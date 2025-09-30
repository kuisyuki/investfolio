from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from application.use_cases.register_user_stock import RegisterUserStockUseCase
from domain.entities.auth import User
from infrastructure.database import get_db
from infrastructure.repositories.user_stock_repository_impl import (
    SQLUserStockRepository,
)
from presentation.dependencies.auth import get_current_user
from presentation.schemas.user_stock import UserStockCreateRequest


router = APIRouter(prefix="/api/user-stocks", tags=["User Stocks"])


class UserStockResponse(BaseModel):
    id: int
    user_stock_id: int
    user_id: int
    ticker_symbol: str
    quantity: int
    acquisition_price: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


@router.get("/", response_model=List[UserStockResponse])
async def get_user_stocks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    ログインユーザーの保有株一覧を取得する

    認証が必要です。ログインユーザーの保有株情報のみ取得できます。
    """
    try:
        repository = SQLUserStockRepository(db)
        user_stocks = await repository.get_by_user_id(current_user.user_id)
        return user_stocks
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"保有株リストの取得に失敗しました: {str(e)}",
        )


@router.post(
    "/", response_model=UserStockResponse, status_code=status.HTTP_201_CREATED
)
async def register_user_stock(
    request: UserStockCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    保有株を登録する

    認証が必要です。ログインユーザーの保有株情報として登録されます。
    """
    try:
        repository = SQLUserStockRepository(db)
        use_case = RegisterUserStockUseCase(repository)

        # 認証されたユーザーのIDを使用
        created_stock = await use_case.execute(
            user_id=current_user.user_id, request=request
        )

        return created_stock
    except Exception as e:
        # 本来はより具体的な例外処理が望ましい
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"予期せぬエラーが発生しました: {str(e)}",
        )
