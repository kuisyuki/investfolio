from fastapi import APIRouter, Depends, HTTPException
from typing import Optional

from application.dto.exchange_rate_dto import ExchangeRateDTO
from application.use_cases.get_usd_jpy_rate import GetUsdJpyRateUseCase
from domain.repositories.exchange_rate_repository import ExchangeRateRepository
from infrastructure.repositories.exchange_rate_repository_impl import ExchangeRateRepositoryImpl
from infrastructure.external.exchange_rate_client import ExchangeRateClient

router = APIRouter(prefix="/api/exchange-rates", tags=["Exchange Rates"])

# Dependency
def get_exchange_rate_repository() -> ExchangeRateRepository:
    client = ExchangeRateClient()
    return ExchangeRateRepositoryImpl(client)

@router.get("/usd-jpy", response_model=Optional[ExchangeRateDTO])
def get_usd_jpy_rate(
    repo: ExchangeRateRepository = Depends(get_exchange_rate_repository)
):
    """
    Get the latest USD/JPY exchange rate.
    """
    use_case = GetUsdJpyRateUseCase(repo)
    result = use_case.execute()
    if not result:
        raise HTTPException(status_code=404, detail="USD/JPY rate not found or API error")
    return result
