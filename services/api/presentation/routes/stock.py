from fastapi import APIRouter, HTTPException, Query
from typing import List
from pydantic import BaseModel
from application.use_cases.get_stock_price import GetStockPriceUseCase
from infrastructure.repositories.mock_stock_repository import MockStockRepository
import httpx

router = APIRouter(prefix="/api/stocks", tags=["stocks"])

class StockSearchResult(BaseModel):
    code: str
    name: str

@router.get("/search", response_model=List[StockSearchResult])
async def search_stocks(keyword: str = Query(..., min_length=1)):
    url = "https://minkabu.jp/api/search/stocks"
    params = {"q": keyword}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

    async with httpx.AsyncClient() as client:
        try:
            print(f"--> Searching for keyword: {keyword}")
            response = await client.get(url, params=params, headers=headers)
            
            print(f"<-- External API status code: {response.status_code}")
            
            response.raise_for_status()
            
            data = response.json()
            # Log only the first 100 characters to avoid flooding the console
            print(f"<-- External API response data (first 100 chars): {str(data)[:100]}")

            search_results = []
            for item in data.get("results", [])[:10]:
                parts = item.get("text", "").split(" ", 1)
                if len(parts) == 2 and parts[0].isdigit():
                    search_results.append(StockSearchResult(code=parts[0], name=parts[1]))
            
            print(f"--> Returning {len(search_results)} results.")
            return search_results

        except httpx.RequestError as e:
            print(f"[ERROR] Request to external API failed: {e}")
            raise HTTPException(status_code=503, detail=f"外部APIへのアクセスに失敗しました: {e}")
        except Exception as e:
            print(f"[ERROR] An unexpected error occurred: {e}")
            raise HTTPException(status_code=500, detail=f"予期せぬエラーが発生しました: {e}")


@router.get("/{stock_code}")
async def get_stock_price(stock_code: str):
    repository = MockStockRepository()
    use_case = GetStockPriceUseCase(repository)
    
    result = await use_case.execute(stock_code)
    
    if not result:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    return result
