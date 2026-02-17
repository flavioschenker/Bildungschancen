from fastapi import status, APIRouter, Depends, HTTPException
from collections.abc import Sequence
from api.utils import PostgresClient
from api.crud import categories
from api.schemas import CategoryCreate, CategoryRead, CategoryDetail
from api.models import Category

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("", response_model=CategoryRead)
async def create_category(
    category_create: CategoryCreate,
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
) -> Category:
    async with postgres_client.get_session() as session:
        category = await categories.create(session, category_create)
        return category
    

@router.get("", response_model=list[CategoryRead])
async def get_categories(
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
) -> Sequence[Category]:
    async with postgres_client.get_session() as session:
        return await categories.read_all(session)


@router.get("/{category_id}", response_model=CategoryDetail)
async def get_category(
    category_id: str,
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
) -> Category:
    async with postgres_client.get_session() as session:
        category = await categories.read(session, category_id)
        if category is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Category with id {category_id} not found!")  
        return category 
    

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: str,
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
) -> None:
    async with postgres_client.get_session() as session:
        category = await categories.delete(session, category_id)
        if category is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Category with id {category_id} not found!")