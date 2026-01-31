from fastapi import APIRouter, Depends, WebSocket
from jai.core import PostgresClient, WebsocketManager
from jai.rag import read_documents, read_document, DocumentRead, DocumentDetailRead

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get("", response_model=list[DocumentRead])
async def get_documents(
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
):
    async with postgres_client.get_session() as session:
        return await read_documents(session)


@router.get("/{document_id}", response_model=DocumentDetailRead)
async def get_document(
    document_id: str,
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
):
    async with postgres_client.get_session() as session:
        return await read_document(session, document_id)