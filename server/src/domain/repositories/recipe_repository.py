from src.domain.entities.recipe import Recipe

from .base_repository import BaseRepository


class RecipeRepository(BaseRepository[Recipe]):
    """Repository to manage CRUD operations on recipes."""

    def __init__(self):
        super().__init__(Recipe)
