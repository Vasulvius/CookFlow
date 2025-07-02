from framefox.core.orm.abstract_entity import AbstractEntity
from sqlmodel import JSON, Column, Field, Relationship


class MealRecipe(AbstractEntity, table=True):
    id: int | None = Field(default=None, primary_key=True)

    meal_id: int = Field(foreign_key="meal.id")
    recipe_id: int = Field(foreign_key="recipe.id")

    servings: int = Field(nullable=False)

    meal: "Meal" = Relationship(back_populates="meal_recipes")
    recipe: "Recipe" = Relationship(back_populates="meal_recipes")
