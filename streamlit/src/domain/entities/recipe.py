from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from src.domain.entities.recipe_ingredient import RecipeIngredient


@dataclass
class Recipe:
    id: UUID
    name: str
    description: str
    ingredients: Optional[list[RecipeIngredient]] = None
