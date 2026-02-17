from fastapi import status, APIRouter, Depends, HTTPException
from collections.abc import Sequence
from api.utils import PostgresClient
from api.crud import units
from api.schemas import UnitCreate, UnitRead, UnitDetail
from api.models import Unit

router = APIRouter(prefix="/units", tags=["Units"])

@router.post("", response_model=UnitRead)
async def create_unit(
    unit_create: UnitCreate,
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
) -> Unit:
    async with postgres_client.get_session() as session:
        unit = await units.create(session, unit_create)
        return unit
    

@router.get("", response_model=list[UnitRead])
async def get_units(
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
) -> Sequence[Unit]:
    async with postgres_client.get_session() as session:
        return await units.read_all(session)


@router.get("/{unit_id}", response_model=UnitDetail)
async def get_unit(
    unit_id: str,
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
) -> Unit:
    async with postgres_client.get_session() as session:
        unit = await units.read(session, unit_id)
        if unit is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Unit with id {unit_id} not found!")  
        return unit 
    

@router.delete("/{unit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_unit(
    unit_id: str,
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
) -> None:
    async with postgres_client.get_session() as session:
        unit = await units.delete(session, unit_id)
        if unit is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Unit with id {unit_id} not found!")