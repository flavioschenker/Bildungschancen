from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from collections.abc import Sequence
from api.models import Skill, UserSkill
from api.schemas import SkillCreate

async def create(session: AsyncSession, skill_create: SkillCreate) -> Skill:
    skill = Skill(
        **skill_create.model_dump()
    )
    session.add(skill)
    await session.commit()
    await session.refresh(skill)
    return skill

async def read_all(session: AsyncSession) -> Sequence[Skill]:
    result = await session.execute(select(Skill))
    return result.scalars().all()

async def read(session: AsyncSession, skill_id: str) -> Skill | None:
    result = await session.execute(
        select(Skill)
        .where(Skill.skill_id == skill_id)
        .options(
            selectinload(Skill.users)
            .joinedload(UserSkill.user)
        )
    )
    return result.scalar_one_or_none()

async def delete(session: AsyncSession, skill_id: str) -> Skill | None:
    result = await session.execute(
        select(Skill)
        .where(Skill.skill_id == skill_id)
    )
    skill = result.scalar_one_or_none()
    if skill:
        try:
            await session.delete(skill)
            await session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="Cannot delete this skill because it is currently assigned to users."
            )
    return skill