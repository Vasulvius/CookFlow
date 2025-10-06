from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.domain.entities.ingredient import Ingredient, IngredientRead
    from src.domain.entities.recipe import Recipe


class RecipeIngredient(SQLModel, table=True):
    """RecipeIngredient entity with SQLModel."""

    __tablename__ = "recipe_ingredients"

    id: UUID = Field(default_factory=uuid4, primary_key=True)

    recipe_id: UUID = Field(foreign_key="recipes.id")
    ingredient_id: UUID = Field(foreign_key="ingredients.id")

    quantity: float = Field()
    unit: str = Field(max_length=50)

    # Relations
    recipe: Recipe = Relationship(back_populates="ingredients")
    ingredient: Ingredient = Relationship(back_populates="recipes")


class RecipeIngredientCreate(SQLModel):
    ingredient_id: UUID
    quantity: float
    unit: str


class RecipeIngredientRead(SQLModel):
    ingredient: IngredientRead
    quantity: float
    unit: str
