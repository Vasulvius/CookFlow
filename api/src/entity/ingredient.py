# from typing import List, Optional

# from sqlmodel import JSON, Field, Relationship, SQLModel

# # from src.entity.recipe import Recipe
# # from src.entity.recipe_ingredient_link import RecipeIngredientLink
# from src.enums import UnitEnum


# class Ingredient(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     name: str = Field(max_length=256, nullable=False)
#     description: str = Field(max_length=256, nullable=True)
#     unit: UnitEnum = Field(nullable=False)
#     # recipes: List[Recipe] = Relationship(
#     #     back_populates="ingredients", link_model=RecipeIngredientLink
#     # )


from typing import Optional

from sqlmodel import Field, SQLModel


class Ingredient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    unit: str
