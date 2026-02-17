from fastapi import status, APIRouter, Depends, HTTPException
from collections.abc import Sequence
from api.utils import PostgresClient
from api.crud import currencies
from api.schemas import CurrencyCreate, CurrencyRead, CurrencyDetail
from api.models import Currency

router = APIRouter(prefix="/currencies", tags=["Currencies"])

@router.post("", response_model=CurrencyRead)
async def create_currency(
    currency_create: CurrencyCreate,
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
) -> Currency:
    async with postgres_client.get_session() as session:
        currency = await currencies.create(session, currency_create)
        return currency
    

@router.get("", response_model=list[CurrencyRead])
async def get_currencies(
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
) -> Sequence[Currency]:
    async with postgres_client.get_session() as session:
        return await currencies.read_all(session)


@router.get("/{currency_id}", response_model=CurrencyDetail)
async def get_currency(
    currency_id: str,
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
) -> Currency:
    async with postgres_client.get_session() as session:
        currency = await currencies.read(session, currency_id)
        if currency is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Currency with id {currency_id} not found!")  
        return currency 
    

@router.delete("/{currency_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_currency(
    currency_id: str,
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
) -> None:
    async with postgres_client.get_session() as session:
        currency = await currencies.delete(session, currency_id)
        if currency is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Currency with id {currency_id} not found!")