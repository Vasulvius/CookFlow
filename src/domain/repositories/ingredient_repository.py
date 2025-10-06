from src.domain.entities.ingredient import Ingredient

from .base_repository import BaseRepository


class IngredientRepository(BaseRepository[Ingredient]):
    """Repository to manage CRUD operations on ingredients."""

    def __init__(self):
        super().__init__(Ingredient)
