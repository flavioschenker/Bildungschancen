from fastapi import status, APIRouter, Depends, HTTPException
from collections.abc import Sequence
from api.utils import PostgresClient
from api.crud import brands
from api.schemas import BrandCreate, BrandRead, BrandDetail
from api.models import Brand

router = APIRouter(prefix="/brands", tags=["Brands"])

@router.post("", response_model=BrandRead)
async def create_brand(
    brand_create: BrandCreate,
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
) -> Brand:
    async with postgres_client.get_session() as session:
        brand = await brands.create(session, brand_create)
        return brand
    

@router.get("", response_model=list[BrandRead])
async def get_brands(
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
) -> Sequence[Brand]:
    async with postgres_client.get_session() as session:
        return await brands.read_all(session)


@router.get("/{brand_id}", response_model=BrandDetail)
async def get_brand(
    brand_id: str,
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
) -> Brand:
    async with postgres_client.get_session() as session:
        brand = await brands.read(session, brand_id)
        if brand is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Brand with id {brand_id} not found!")  
        return brand 
    

@router.delete("/{brand_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_brand(
    brand_id: str,
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
) -> None:
    async with postgres_client.get_session() as session:
        brand = await brands.delete(session, brand_id)
        if brand is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Brand with id {brand_id} not found!")