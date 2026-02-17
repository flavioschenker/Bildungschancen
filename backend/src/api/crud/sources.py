from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from collections.abc import Sequence
from api.models import Source
from api.schemas import SourceCreate

async def create(session: AsyncSession, source_create: SourceCreate) -> Source:
    source = Source(
        **source_create.model_dump()
    )
    session.add(source)
    await session.commit()
    await session.refresh(source)
    return source

async def read_all(session: AsyncSession) -> Sequence[Source]:
    result = await session.execute(select(Source))
    return result.scalars().all()

async def read(session: AsyncSession, source_id: str) -> Source | None:
    result = await session.execute(
        select(Source)
        .where(Source.source_id == source_id)
        .options(selectinload(Source.ingredients))
    )
    return result.scalar_one_or_none()

async def delete(session: AsyncSession, source_id: str) -> Source | None:
    result = await session.execute(
        select(Source)
        .where(Source.source_id == source_id)
    )
    source = result.scalar_one_or_none()
    if source:
        try:
            await session.delete(source)
            await session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="Cannot delete this source because it is currently assigned to one or more ingredients."
            )
    return source