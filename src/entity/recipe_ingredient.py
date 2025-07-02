from framefox.core.orm.abstract_entity import AbstractEntity
from sqlmodel import JSON, Column, Field, Relationship


class RecipeIngredient(AbstractEntity, table=True):
    id: int | None = Field(default=None, primary_key=True)

    recipe_id: "Recipe" = Relationship(back_populates="recipe_ingredients")

    ingredient_id: "Ingredient" = Relationship(back_populates="recipe_ingredients")
    quantity: float = Field(nullable=False)
    unit: str = Field(max_length=256, nullable=False)
