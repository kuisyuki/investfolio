from typing import Optional, Dict
from domain.repositories.exchange_rate_repository import ExchangeRateRepository
from infrastructure.external.exchange_rate_client import ExchangeRateClient

class ExchangeRateRepositoryImpl(ExchangeRateRepository):
    def __init__(self, client: ExchangeRateClient):
        self.client = client

    def get_usd_jpy_rate(self) -> Optional[Dict]:
        rate = self.client.get_usd_jpy_rate()
        if rate is not None:
            return {
                "symbol": "USD/JPY",
                "last": f"{rate:.2f}",
            }
        return None
