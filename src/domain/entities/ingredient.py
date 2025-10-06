from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.domain.entities.recipe_ingredient import RecipeIngredient


class Ingredient(SQLModel, table=True):
    """Ingredient entity with SQLModel."""

    __tablename__ = "ingredients"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(max_length=255)
    description: str = Field()

    recipes: list[RecipeIngredient] = Relationship(back_populates="ingredient")


class IngredientRead(SQLModel):
    id: UUID
    name: str
    description: str
