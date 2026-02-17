from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from collections.abc import Sequence
from api.models import Currency
from api.schemas import CurrencyCreate

async def create(session: AsyncSession, currency_create: CurrencyCreate) -> Currency:
    currency = Currency(
        **currency_create.model_dump()
    )
    session.add(currency)
    await session.commit()
    await session.refresh(currency)
    return currency

async def read_all(session: AsyncSession) -> Sequence[Currency]:
    result = await session.execute(select(Currency))
    return result.scalars().all()

async def read(session: AsyncSession, currency_id: str) -> Currency | None:
    result = await session.execute(
        select(Currency)
        .where(Currency.currency_id == currency_id)
        .options(selectinload(Currency.ingredients))
    )
    return result.scalar_one_or_none()

async def delete(session: AsyncSession, currency_id: str) -> Currency | None:
    result = await session.execute(
        select(Currency)
        .where(Currency.currency_id == currency_id)
    )
    currency = result.scalar_one_or_none()
    if currency:
        try:
            await session.delete(currency)
            await session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="Cannot delete this currency because it is currently assigned to one or more ingredients."
            )
    return currency