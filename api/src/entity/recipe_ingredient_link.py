from sqlmodel import JSON, Field, Relationship, SQLModel
from src.entity.ingredient import Ingredient
from src.enums import UnitEnum


class RecipeIngredientLink(SQLModel, table=True):
    recipe_id: int | None = Field(
        default=None, foreign_key="recipe.id", primary_key=True)
    ingredient_id: int = Field(
        nullable=False, foreign_key="ingredient.id", primary_key=True)
    quantity: float = Field(nullable=False)
    unit: UnitEnum = Field(nullable=False)
