from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from api.utils import PostgresClient, WebsocketManager
from api.routes import router_users


def create_app(
    postgres_client: PostgresClient,
    websocket_manager: WebsocketManager,
):
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        async with (
            postgres_client,
            websocket_manager,
        ):
            postgres_client.bind_fastapi(app)
            websocket_manager.bind_fastapi(app)

            await postgres_client.create_tables()
            yield

    app = FastAPI(title="JAI API", lifespan=lifespan)
    app.include_router(router_users)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost",
            "http://localhost:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    async def root():
        return {
            "app": "Bildungschance API",
            "description": "JAI Central API",
            "documentation": "/docs",
            "status": "operational",
            "version": "v1.0.0"
        }

    @app.get("/health")
    async def health():
        if not await postgres_client.ping():
            return JSONResponse(
                status_code=503, content={"status": "unhealthy", "database": "down"}
            )

        return {"status": "healthy", "version": "v1.0.0"}

    return app
