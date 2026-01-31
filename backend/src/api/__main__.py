import uvicorn
from api.utils import PostgresClient, WebsocketManager
from api.config import settings
from api.app import create_app


if __name__ == "__main__":
    postgres_client = PostgresClient(
        host=settings.postgres_host,
        port=settings.postgres_port,
        user=settings.postgres_user,
        password=settings.postgres_password,
        db=settings.postgres_db,
    )
    websocket_manager = WebsocketManager()
    app = create_app(
        postgres_client=postgres_client,
        websocket_manager=websocket_manager,
    )
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )
