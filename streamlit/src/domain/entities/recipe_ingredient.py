from dataclasses import dataclass
from uuid import UUID


@dataclass
class RecipeIngredient:
    id: UUID

    recipe_id: UUID
    ingredient_id: UUID

    quantity: float
    unit: str
