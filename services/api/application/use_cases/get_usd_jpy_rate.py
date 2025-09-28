from typing import Optional
from domain.repositories.exchange_rate_repository import ExchangeRateRepository
from application.dto.exchange_rate_dto import ExchangeRateDTO

class GetUsdJpyRateUseCase:
    def __init__(self, exchange_rate_repository: ExchangeRateRepository):
        self.exchange_rate_repository = exchange_rate_repository

    def execute(self) -> Optional[ExchangeRateDTO]:
        rate_data = self.exchange_rate_repository.get_usd_jpy_rate()
        if rate_data:
            return ExchangeRateDTO(**rate_data)
        return None
