from contextlib import asynccontextmanager
from typing import AsyncIterator, Self
from fastapi import FastAPI, Request
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,
)
from api.utils.logging import logger

class PostgresBase(DeclarativeBase):
    pass


class PostgresClient:
    def __init__(self, host: str, port: int, user: str, password: str, db: str) -> None:
        self.url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"
        self.engine: None | AsyncEngine = None
        self.session_factory: None | async_sessionmaker[AsyncSession] = None

    async def __aenter__(self) -> Self:
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> bool:
        await self.close()
        return False

    async def connect(self) -> None:
        if self.engine is None:
            self.engine = create_async_engine(self.url)

            self.session_factory = async_sessionmaker(
                bind=self.engine, expire_on_commit=False
            )
            logger.debug("[Postgres Client] Connection established.")

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        if not self.session_factory:
            raise RuntimeError(
                "Client is not connected. Call connect() or use 'async with client'."
            )

        session = self.session_factory()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def close(self):
        if self.engine:
            await self.engine.dispose()
            self.engine = None
            self.session_factory = None
            logger.debug("[Postgres Client] Connection closed.")

    def bind_fastapi(self, app: FastAPI):
        app.state.postgres_connection = self

    @classmethod
    def from_fastapi(cls, request: Request):
        return request.app.state.postgres_connection

    async def create_tables(self) -> None:
        """
        Creates all tables defined in PostgresBase metadata.

        CRITICAL: Ensure all Model classes (e.g. Document, User) are imported
        in the application BEFORE this method is called, otherwise
        SQLAlchemy won't know they exist.
        """
        if not self.engine:
            raise RuntimeError("Engine not initialized. Call connect() first.")

        logger.info("[Postgres Client] Checking and creating missing tables...")

        async with self.engine.begin() as conn:
            await conn.run_sync(PostgresBase.metadata.create_all)

        logger.info("[Postgres Client] Table creation check complete.")

    async def ping(self) -> bool:
        """
        Verifies the database connection is alive.
        Returns True if successful, False otherwise.
        """
        if not self.engine:
            logger.error("[Postgres Client] Ping failed: Engine not initialized.")
            return False

        try:
            async with self.get_session() as session:
                await session.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.error(f"[Postgres Client] Health check failed: {e}")
            return False
