from framefox.core.orm.abstract_entity import AbstractEntity
from sqlmodel import JSON, Column, Field, Relationship


class RecipeIngredient(AbstractEntity, table=True):
    id: int | None = Field(default=None, primary_key=True)

    recipe_id: int = Field(foreign_key="recipe.id")
    ingredient_id: int = Field(foreign_key="ingredient.id")

    quantity: float = Field(nullable=False)
    unit: str = Field(max_length=256, nullable=False)

    recipe: "Recipe" = Relationship(back_populates="recipe_ingredients")
    ingredient: "Ingredient" = Relationship(back_populates="recipe_ingredients")
