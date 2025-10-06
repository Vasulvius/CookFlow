from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from src.domain.entities.recipe_ingredient import (
        RecipeIngredient,
        RecipeIngredientCreate,
        RecipeIngredientRead,
    )


class Recipe(SQLModel, table=True):
    """Recipe entity with SQLModel."""

    __tablename__ = "recipes"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(max_length=255)
    description: str = Field()

    # Relation many-to-many with attributs
    ingredients: list[RecipeIngredient] = Relationship(back_populates="recipe")


class RecipeCreate(SQLModel):
    """Model for creating a recipe."""

    name: str = Field(max_length=255)
    description: str = Field()
    ingredients: list[RecipeIngredientCreate] = []


class RecipeRead(SQLModel):
    """Model for reading a recipe."""

    id: UUID
    name: str
    description: str
    ingredients: list[RecipeIngredientRead]


class RecipeUpdate(SQLModel):
    """Model for updating a recipe."""

    name: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None)
