from fastapi import status, APIRouter, Depends, HTTPException
from collections.abc import Sequence
from api.utils import PostgresClient
from api.crud import sources
from api.schemas import SourceCreate, SourceRead, SourceDetail
from api.models import Source

router = APIRouter(prefix="/sources", tags=["Sources"])

@router.post("", response_model=SourceRead)
async def create_source(
    source_create: SourceCreate,
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
) -> Source:
    async with postgres_client.get_session() as session:
        source = await sources.create(session, source_create)
        return source
    

@router.get("", response_model=list[SourceRead])
async def get_sources(
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
) -> Sequence[Source]:
    async with postgres_client.get_session() as session:
        return await sources.read_all(session)


@router.get("/{source_id}", response_model=SourceDetail)
async def get_source(
    source_id: str,
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
) -> Source:
    async with postgres_client.get_session() as session:
        source = await sources.read(session, source_id)
        if source is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Source with id {source_id} not found!")  
        return source 
    

@router.delete("/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_source(
    source_id: str,
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
) -> None:
    async with postgres_client.get_session() as session:
        source = await sources.delete(session, source_id)
        if source is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Source with id {source_id} not found!")