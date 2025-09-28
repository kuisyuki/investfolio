from abc import ABC, abstractmethod
from typing import Optional, Dict

class ExchangeRateRepository(ABC):
    @abstractmethod
    def get_usd_jpy_rate(self) -> Optional[Dict]:
        pass
