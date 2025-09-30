from domain.entities.user_stock import UserStock
from domain.repositories.user_stock_repository import UserStockRepository
from presentation.schemas.user_stock import UserStockCreateRequest


class RegisterUserStockUseCase:
    """保有株を登録するユースケース"""

    def __init__(self, user_stock_repository: UserStockRepository):
        self.user_stock_repository = user_stock_repository

    async def execute(self, user_id: int, request: UserStockCreateRequest) -> UserStock:
        """ユースケースの実行"""

        # 今後、ここにビジネスロジックを追加できる
        # (例: ユーザーが既に同じ銘柄を登録済みかチェックするなど)

        user_stock_to_create = UserStock(
            id=None,  # IDはリポジトリ層で生成される
            user_stock_id=None,  # リポジトリ層でidと同じ値を設定
            user_id=user_id,
            ticker_symbol=request.ticker_symbol,
            quantity=request.quantity,
            acquisition_price=request.acquisition_price,
        )

        created_stock = await self.user_stock_repository.create(user_stock_to_create)
        return created_stock
