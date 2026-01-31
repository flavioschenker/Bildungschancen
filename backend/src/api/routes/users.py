from fastapi import APIRouter, Depends, WebSocket
from api.crud import read_users, read_user, create_user
from api.utils import PostgresClient, WebsocketManager
from api.schemas import UserRead, UserCreate, UserDetailRead


router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get("", response_model=list[UserRead])
async def get_users(
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
) -> list[UserRead]:
    async with postgres_client.get_session() as session:
        return await read_users(session)

@router.post("", response_model=str)
async def post_user(
    user_create: UserCreate,
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
) -> str:
    async with postgres_client.get_session() as session:
        user = await create_user(session, user_create)
        return user.user_id


@router.get("/{user_id}", response_model=UserDetailRead)
async def get_user(
    document_id: str,
    postgres_client: PostgresClient = Depends(PostgresClient.from_fastapi),
) -> UserDetailRead:
    async with postgres_client.get_session() as session:
        return await read_user(session, document_id)
    

@router.websocket("")
async def connect(
    websocket: WebSocket,
    manager: WebsocketManager = Depends(WebsocketManager.from_fastapi),
) -> None:
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except Exception:
        manager.disconnect(websocket)
