from typing import List

from sqlmodel import JSON, Field, Relationship, SQLModel
from src.entity.ingredient import Ingredient
from src.entity.recipe_ingredient_link import RecipeIngredientLink


class Recipe(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=256, nullable=False)
    description: str = Field(max_length=256, nullable=True)
    # ingredients: List[Ingredient] = Relationship(
    #     back_populates="recipes", link_model=RecipeIngredientLink
    # )
