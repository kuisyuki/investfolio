from fastapi import APIRouter, HTTPException
from application.use_cases.get_stock_price import GetStockPriceUseCase
from infrastructure.repositories.mock_stock_repository import MockStockRepository

router = APIRouter(prefix="/api/stocks", tags=["stocks"])

@router.get("/nintendo")
async def get_nintendo_stock_price():
    repository = MockStockRepository()
    use_case = GetStockPriceUseCase(repository)
    
    result = await use_case.execute("7974")
    
    if not result:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    return result