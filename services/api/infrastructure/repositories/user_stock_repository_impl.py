import uuid

from domain.entities.user_stock import UserStock
from domain.repositories.user_stock_repository import UserStockRepository
from infrastructure.models.user_stock import UserStockModel
from sqlalchemy.orm import Session


class SQLUserStockRepository(UserStockRepository):
    """SQLAlchemyを使用した保有株リポジトリの実装"""

    def __init__(self, db: Session):
        self.db = db

    async def create(self, user_stock: UserStock) -> UserStock:
        """保有株を作成"""
        user_stock_model = UserStockModel(
            id=str(uuid.uuid4()),
            user_id=user_stock.user_id,
            ticker_symbol=user_stock.ticker_symbol,
            quantity=user_stock.quantity,
            acquisition_price=user_stock.acquisition_price,
        )

        self.db.add(user_stock_model)
        self.db.commit()
        self.db.refresh(user_stock_model)

        return self._model_to_entity(user_stock_model)

    def _model_to_entity(self, model: UserStockModel) -> UserStock:
        """モデルをエンティティに変換"""
        return UserStock(
            id=model.id,
            user_id=model.user_id,
            ticker_symbol=model.ticker_symbol,
            quantity=model.quantity,
            acquisition_price=float(model.acquisition_price),  # DECIMALをfloatに変換
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
