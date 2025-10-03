from abc import ABC
from typing import Generic, List, Type, TypeVar
from uuid import UUID

from sqlmodel import SQLModel, select

from src.infrastructure.database import db_manager

T = TypeVar("T", bound=SQLModel)


class BaseRepository(Generic[T], ABC):
    """Repository de base avec les opérations CRUD communes."""

    def __init__(self, model: Type[T]):
        self.model = model

    async def add(self, entity: T) -> T:
        """Ajoute une nouvelle entité à la base de données."""
        async with db_manager.get_session() as session:
            session.add(entity)
            await session.commit()
            await session.refresh(entity)
            return entity

    async def get_all(self) -> List[T]:
        """Récupère toutes les entités de la base de données."""
        async with db_manager.get_session() as session:
            result = await session.exec(select(self.model))
            return list(result.all())

    async def get_by_id(self, entity_id: UUID) -> T | None:
        """Récupère une entité par son ID."""
        async with db_manager.get_session() as session:
            result = await session.exec(select(self.model).where(self.model.id == entity_id))
            return result.first()

    async def update(self, entity: T) -> T:
        """Met à jour une entité existante dans la base de données."""
        async with db_manager.get_session() as session:
            merged_entity = await session.merge(entity)
            await session.commit()
            await session.refresh(merged_entity)
            return merged_entity

    async def delete(self, entity_id: UUID) -> bool:
        """Supprime une entité de la base de données."""
        async with db_manager.get_session() as session:
            result = await session.exec(select(self.model).where(self.model.id == entity_id))
            entity = result.first()
            if entity:
                await session.delete(entity)
                await session.commit()
                return True
            return False

    async def delete_entity(self, entity: T) -> bool:
        """Supprime une entité directement."""
        async with db_manager.get_session() as session:
            await session.delete(entity)
            await session.commit()
            return True
