from framefox.core.orm.abstract_entity import AbstractEntity
from sqlmodel import JSON, Column, Field, Relationship


class Meal(AbstractEntity, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=256, nullable=False)
    notes: str = Field(max_length=256, nullable=True)

    meal_recipes: "MealRecipe" = Relationship(back_populates="meal_id")
