from typing import List

from framefox.core.orm.abstract_entity import AbstractEntity
from sqlmodel import JSON, Column, Field, Relationship


class Meal(AbstractEntity, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=256, nullable=False)
    notes: str = Field(max_length=256, nullable=True)

    meal_recipes: List["MealRecipe"] = Relationship(back_populates="meal", cascade_delete=True)
