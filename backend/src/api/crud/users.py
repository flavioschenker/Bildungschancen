from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from collections.abc import Sequence
from api.models import User, Skill, UserSkill
from api.schemas import UserCreate, UserUpdate

async def create(session: AsyncSession, user_create: UserCreate) -> User:
    hashed_password = user_create.password + "_hashed"
    user_data = user_create.model_dump(exclude={"password", "skill_ids"})
    user = User(
        **user_data,
        password_hash=hashed_password,
    )
    if user_create.skill_ids:
        result = await session.execute(
            select(Skill)
            .where(Skill.skill_id.in_(user_create.skill_ids))
        )
        skills = result.scalars().all()
        for skill in skills:
            user.skills.append(
                UserSkill(skill=skill)
            )
    else:
        user.skills = []
    session.add(user)            
    await session.commit()
    await session.refresh(user, ["id", "created_at", "updated_at"])
    return user

async def read_all(session: AsyncSession) -> Sequence[User]:
    result = await session.execute(select(User))
    return result.scalars().all()

async def read(session: AsyncSession, user_id: str) -> User | None:
    result = await session.execute(
        select(User)
        .where(User.user_id == user_id)
        .options(
            selectinload(User.skills)
            .joinedload(UserSkill.skill)
        )
    )
    return result.scalar_one_or_none()

async def update(session: AsyncSession, user_id: str, user_update: UserUpdate) -> User | None:
    user = await read(session, user_id)
    if user:
        update_data = user_update.model_dump(exclude_unset=True)
        skill_ids = update_data.pop("skill_ids", None)
        for key, value in update_data.items():
            setattr(user, key, value)
        if skill_ids:
            user.skills.clear()
            result = await session.execute(
                select(Skill)
                .where(Skill.skill_id.in_(skill_ids))
            )
            skills = result.scalars().all()
            for skill in skills:
                user.skills.append(
                    UserSkill(skill=skill)
                )
        await session.commit()
        await session.refresh(user, ["updated_at"])
    return user

async def delete(session: AsyncSession, user_id: str) -> User | None:
    result = await session.execute(
        select(User)
        .where(User.user_id == user_id))
    user = result.scalar_one_or_none()
    if user:
        await session.delete(user)
        await session.commit()
    return user