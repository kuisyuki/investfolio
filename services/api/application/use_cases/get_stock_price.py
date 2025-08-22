from typing import Optional
from domain.repositories.stock_repository import StockRepository
from application.dto.stock_dto import StockPriceResponse

class GetStockPriceUseCase:
    def __init__(self, stock_repository: StockRepository):
        self.stock_repository = stock_repository
    
    async def execute(self, symbol: str) -> Optional[StockPriceResponse]:
        stock = await self.stock_repository.get_stock_price(symbol)
        if stock:
            return StockPriceResponse(
                symbol=stock.symbol,
                name=stock.name,
                price=stock.price,
                currency=stock.currency,
                timestamp=stock.timestamp,
                message=f"{stock.name}の株価は{stock.price:,.0f}円です"
            )
        return None