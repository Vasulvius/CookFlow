from typing import List, Optional
from uuid import UUID

from api.ingredient.domain.ingredient import Ingredient
from api.ingredient.infrastructure.ingredient_repository import IngredientRepository


class IngredientService:
    """Service for ingredient business logic."""

    def __init__(self):
        self.repository = IngredientRepository()

    def create_ingredient(self, name: str, category: Optional[str] = None) -> Ingredient:
        """Create a new ingredient."""
        return self.repository.create(name=name, category=category)

    def get_ingredient(self, ingredient_id: UUID) -> Optional[Ingredient]:
        """Get an ingredient by ID."""
        return self.repository.get_by_id(ingredient_id)

    def list_ingredients(self) -> List[Ingredient]:
        """List all ingredients."""
        return self.repository.list_all()

    def update_ingredient(
        self, ingredient_id: UUID, name: Optional[str] = None, category: Optional[str] = None
    ) -> Optional[Ingredient]:
        """Update an ingredient."""
        return self.repository.update(ingredient_id, name=name, category=category)

    def delete_ingredient(self, ingredient_id: UUID) -> bool:
        """Delete an ingredient."""
        return self.repository.delete(ingredient_id)
