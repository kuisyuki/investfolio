from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from application.use_cases.register_user_stock import RegisterUserStockUseCase
from infrastructure.database import get_db
from infrastructure.repositories.user_stock_repository_impl import (
    SQLUserStockRepository,
)
from presentation.schemas.user_stock import UserStockCreateRequest


router = APIRouter(prefix="/api/user-stocks", tags=["User Stocks"])


class UserStockResponse(BaseModel):
    id: str
    user_id: str
    ticker_symbol: str
    quantity: int
    acquisition_price: float
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


@router.post(
    "/", response_model=UserStockResponse, status_code=status.HTTP_201_CREATED
)
async def register_user_stock(
    request: UserStockCreateRequest, db: Session = Depends(get_db)
):
    """
    保有株を登録する (一時的な実装、認証なし)

    **警告:** このエンドポイントは認証機能がないため安全ではありません。
    開発目的でのみ使用してください。
    """
    try:
        repository = SQLUserStockRepository(db)
        use_case = RegisterUserStockUseCase(repository)

        created_stock = await use_case.execute(user_id=request.user_id, request=request)

        return created_stock
    except Exception as e:
        # 本来はより具体的な例外処理が望ましい
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"予期せぬエラーが発生しました: {str(e)}",
        )
