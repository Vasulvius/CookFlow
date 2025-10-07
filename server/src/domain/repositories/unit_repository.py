from src.domain.entities.unit import Unit

from .base_repository import BaseRepository


class UnitRepository(BaseRepository[Unit]):
    """Repository pour gérer les opérations CRUD sur les unités."""

    def __init__(self):
        super().__init__(Unit)
