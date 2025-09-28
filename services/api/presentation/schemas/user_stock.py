from pydantic import BaseModel, Field

class UserStockCreateRequest(BaseModel):
    user_id: str = Field(..., description="ユーザーID")
    ticker_symbol: str = Field(..., description="銘柄コード")
    quantity: int = Field(..., gt=0, description="保有株数")
    acquisition_price: float = Field(..., gt=0, description="取得単価")
