from src.entities.recipe import Recipe

from .base_repository import BaseRepository


class RecipeRepository(BaseRepository[Recipe]):
    """Repository pour gérer les opérations CRUD sur les recettes."""

    def __init__(self):
        super().__init__(Recipe)
