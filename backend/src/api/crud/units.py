from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from collections.abc import Sequence
from api.models import Unit
from api.schemas import UnitCreate

async def create(session: AsyncSession, unit_create: UnitCreate) -> Unit:
    unit = Unit(
        **unit_create.model_dump()
    )
    session.add(unit)
    await session.commit()
    await session.refresh(unit)
    return unit

async def read_all(session: AsyncSession) -> Sequence[Unit]:
    result = await session.execute(select(Unit))
    return result.scalars().all()

async def read(session: AsyncSession, unit_id: str) -> Unit | None:
    result = await session.execute(
        select(Unit)
        .where(Unit.unit_id == unit_id)
        .options(selectinload(Unit.base_unit_ingredients))
    )
    return result.scalar_one_or_none()

async def delete(session: AsyncSession, unit_id: str) -> Unit | None:
    result = await session.execute(
        select(Unit)
        .where(Unit.unit_id == unit_id)
    )
    unit = result.scalar_one_or_none()
    if unit:
        try:
            await session.delete(unit)
            await session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="Cannot delete this unit because it is currently assigned to one or more ingredients."
            )
    return unit