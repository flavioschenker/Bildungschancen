from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from api.models import User
from api.schemas import UserRead, UserCreate, UserDetailRead

async def read_users(session: AsyncSession) -> list[UserRead]:
    result = await session.execute(select(User))
    return result.scalars().all()

async def read_user(session: AsyncSession, user_id: str) -> UserDetailRead:
    result = await session.execute(
        select(User)
        .where(User.user_id == user_id)
        .options(selectinload(User.skills)) # some relationship details
    )
    return result.scalar_one_or_none()

async def create_user(session: AsyncSession, user_create: UserCreate) -> User:
    user = User(
        first_name=user_create.first_name,
        last_name=user_create.last_name
    )
    session.add(user)
    await session.flush() # push to Database create user_id
    await session.refresh(user) # refresh python object with created user_id
    return user