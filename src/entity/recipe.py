from typing import List

from framefox.core.orm.abstract_entity import AbstractEntity
from sqlmodel import JSON, Column, Field, Relationship


class Recipe(AbstractEntity, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=256, nullable=False)
    description: str = Field(max_length=256, nullable=True)

    recipe_ingredients: List["RecipeIngredient"] = Relationship(back_populates="recipe", cascade_delete=True)
    meal_recipes: List["MealRecipe"] = Relationship(back_populates="recipe", cascade_delete=True)
