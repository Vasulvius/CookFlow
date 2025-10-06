from abc import ABC
from typing import Generic, List, Type, TypeVar
from uuid import UUID

from sqlmodel import SQLModel, select

from src.infrastructure import db_manager

T = TypeVar("T", bound=SQLModel)


class BaseRepository(Generic[T], ABC):
    """Base repository with common CRUD operations."""

    def __init__(self, model: Type[T]):
        self.model = model

    async def exists(self, entity_id: UUID) -> bool:
        """Check if an entity exists by its ID."""
        async with db_manager.get_session() as session:
            result = await session.exec(select(self.model).where(self.model.id == entity_id))
            return result.first() is not None

    async def add(self, entity: T) -> T:
        """Adds a new entity to the database."""
        async with db_manager.get_session() as session:
            session.add(entity)
            await session.commit()
            await session.refresh(entity)
            return entity

    async def get_all(self) -> List[T]:
        """Retrieves all entities from the database."""
        async with db_manager.get_session() as session:
            result = await session.exec(select(self.model))
            return list(result.all())

    async def get_by_id(self, entity_id: UUID) -> T | None:
        """Retrieves an entity by its ID."""
        async with db_manager.get_session() as session:
            result = await session.exec(select(self.model).where(self.model.id == entity_id))
            return result.first()

    async def update(self, entity: T) -> T:
        """Updates an existing entity in the database."""
        async with db_manager.get_session() as session:
            merged_entity = await session.merge(entity)
            await session.commit()
            await session.refresh(merged_entity)
            return merged_entity

    async def delete(self, entity_id: UUID) -> bool:
        """Deletes an entity from the database."""
        async with db_manager.get_session() as session:
            result = await session.exec(select(self.model).where(self.model.id == entity_id))
            entity = result.first()
            if entity:
                await session.delete(entity)
                await session.commit()
                return True
            return False

    async def delete_entity(self, entity: T) -> bool:
        """Deletes an entity directly."""
        async with db_manager.get_session() as session:
            await session.delete(entity)
            await session.commit()
            return True
