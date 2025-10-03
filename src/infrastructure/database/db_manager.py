from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from ...config.settings import get_settings


class DatabaseManager:
    """Gestionnaire de base de données avec SQLModel."""

    def __init__(self):
        settings = get_settings()
        self.engine = create_async_engine(
            settings.database_url,
            echo=settings.debug,
            connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
        )
        self.session_factory = async_sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    async def create_tables(self):
        """Créer toutes les tables."""
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Générateur de session de base de données."""
        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def close(self):
        """Fermer le moteur de base de données."""
        await self.engine.dispose()


db_manager = DatabaseManager()
