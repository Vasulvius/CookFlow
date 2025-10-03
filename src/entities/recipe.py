from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Recipe(SQLModel, table=True):
    """Entité Recipe avec SQLModel."""

    __tablename__ = "recipes"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(max_length=255)
    description: str = Field()


class RecipeCreate(SQLModel):
    """Modèle pour la création d'une recette."""

    name: str = Field(max_length=255)
    description: str = Field()


class RecipeRead(SQLModel):
    """Modèle pour la lecture d'une recette."""

    id: UUID
    name: str
    description: str


class RecipeUpdate(SQLModel):
    """Modèle pour la mise à jour d'une recette."""

    name: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None)
