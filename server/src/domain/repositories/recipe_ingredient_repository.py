from src.domain.entities.recipe_ingredient import RecipeIngredient

from .base_repository import BaseRepository


class RecipeIngredientRepository(BaseRepository[RecipeIngredient]):
    """Repository to manage CRUD operations on recipe ingredients."""

    def __init__(self):
        super().__init__(RecipeIngredient)
