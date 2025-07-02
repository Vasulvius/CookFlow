from framefox.core.orm.abstract_entity import AbstractEntity
from sqlmodel import JSON, Column, Field, Relationship


class MealRecipe(AbstractEntity, table=True):
    id: int | None = Field(default=None, primary_key=True)

    meal_id: "Meal" = Relationship(back_populates="meal_recipes")

    recipe_id: "Recipe" = Relationship(back_populates="meal_recipes")
    servings: int = Field(nullable=False)
