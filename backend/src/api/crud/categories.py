from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from collections.abc import Sequence
from api.models import Category
from api.schemas import CategoryCreate

async def create(session: AsyncSession, category_create: CategoryCreate) -> Category:
    category = Category(
        **category_create.model_dump()
    )
    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category

async def read_all(session: AsyncSession) -> Sequence[Category]:
    result = await session.execute(select(Category))
    return result.scalars().all()

async def read(session: AsyncSession, category_id: str) -> Category | None:
    result = await session.execute(
        select(Category)
        .where(Category.category_id == category_id)
        .options(selectinload(Category.ingredients))
    )
    return result.scalar_one_or_none()

async def delete(session: AsyncSession, category_id: str) -> Category | None:
    result = await session.execute(
        select(Category)
        .where(Category.category_id == category_id)
    )
    category = result.scalar_one_or_none()
    if category:
        try:
            await session.delete(category)
            await session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="Cannot delete this category because it is currently assigned to one or more ingredients."
            )
    return category