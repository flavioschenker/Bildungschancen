from fastapi import status, APIRouter, Depends, HTTPException
from collections.abc import Sequence
from api.crud import users
from api.utils import PostgresClient
from api.schemas import UserCreate, UserRead, UserDetail, UserUpdate
from api.models import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("", response_model=UserDetail)
async def create_user(
    user_create: UserCreate,
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
) -> User:
    async with postgres_client.get_session() as session:
        user = await users.create(session, user_create)
        return user

@router.get("", response_model=list[UserRead])
async def get_users(
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
) -> Sequence[User]:
    async with postgres_client.get_session() as session:
        return await users.read_all(session)

@router.get("/{user_id}", response_model=UserDetail)
async def get_user(
    user_id: str,
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
) -> User:
    async with postgres_client.get_session() as session:
        user = await users.read(session, user_id)
        if user is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found!")  
        return user 
    
@router.patch("/{user_id}", response_model=UserDetail)
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
) -> User:
    async with postgres_client.get_session() as session:
        user = await users.update(session, user_id, user_update)
        if user is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found!")  
        return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
) -> None:
    async with postgres_client.get_session() as session:
        user = await users.delete(session, user_id)
        if user is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found!")