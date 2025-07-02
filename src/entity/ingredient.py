from framefox.core.orm.abstract_entity import AbstractEntity
from sqlmodel import JSON, Column, Field, Relationship


class Ingredient(AbstractEntity, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=256, nullable=False)
    category: str = Field(max_length=256, nullable=True)

    recipe_ingredients: "RecipeIngredient" = Relationship(back_populates="ingredient_id")
