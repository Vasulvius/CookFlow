from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from .settings import get_settings


class DatabaseManager:
    """Database manager with SQLModel."""

    def __init__(self):
        settings = get_settings()
        self.engine = create_async_engine(
            settings.database_url,
            echo=settings.debug,
            connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
        )
        self.session_factory = async_sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)  # SQLModel AsyncSession

    async def create_tables(self):
        """Create all tables."""
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Context manager to obtain a database session."""
        async with self.session_factory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise

    async def close(self):
        """Close the database engine."""
        await self.engine.dispose()


db_manager = DatabaseManager()
