from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from collections.abc import Sequence
from api.models import Brand
from api.schemas import BrandCreate

async def create(session: AsyncSession, brand_create: BrandCreate) -> Brand:
    brand = Brand(
        **brand_create.model_dump()
    )
    session.add(brand)
    await session.commit()
    await session.refresh(brand)
    return brand

async def read_all(session: AsyncSession) -> Sequence[Brand]:
    result = await session.execute(select(Brand))
    return result.scalars().all()

async def read(session: AsyncSession, brand_id: str) -> Brand | None:
    result = await session.execute(
        select(Brand)
        .where(Brand.brand_id == brand_id)
        .options(selectinload(Brand.ingredients))
    )
    return result.scalar_one_or_none()

async def delete(session: AsyncSession, brand_id: str) -> Brand | None:
    result = await session.execute(
        select(Brand)
        .where(Brand.brand_id == brand_id)
    )
    brand = result.scalar_one_or_none()
    if brand:
        try:
            await session.delete(brand)
            await session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="Cannot delete this brand because it is currently assigned to one or more ingredients."
            )
    return brand