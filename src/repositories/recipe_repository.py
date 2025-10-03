from uuid import UUID

from sqlmodel import select

from src.entities.recipe import Recipe
from src.infrastructure.database import db_manager


class RecipeRepository:
    """Repository pour gérer les opérations CRUD sur les recettes."""

    @staticmethod
    async def add(recipe: Recipe) -> Recipe:
        """Ajoute une nouvelle recette à la base de données."""
        async with db_manager.get_session() as session:
            session.add(recipe)
            await session.commit()
            await session.refresh(recipe)
            return recipe

    @staticmethod
    async def get_all() -> list[Recipe]:
        """Récupère toutes les recettes de la base de données."""
        async with db_manager.get_session() as session:
            result = await session.exec(select(Recipe))
            return list(result.all())

    @staticmethod
    async def get_by_id(recipe_id: UUID) -> Recipe | None:
        """Récupère une recette par son ID."""
        async with db_manager.get_session() as session:
            result = await session.exec(select(Recipe).where(Recipe.id == recipe_id))
            return result.first()

    @staticmethod
    async def update(recipe: Recipe) -> Recipe:
        """Met à jour une recette existante dans la base de données."""
        async with db_manager.get_session() as session:
            merged_recipe = await session.merge(recipe)
            await session.commit()
            await session.refresh(merged_recipe)
            return merged_recipe

    @staticmethod
    async def delete(recipe_id: UUID) -> bool:
        """Supprime une recette de la base de données."""
        async with db_manager.get_session() as session:
            result = await session.exec(select(Recipe).where(Recipe.id == recipe_id))
            recipe = result.first()
            if recipe:
                await session.delete(recipe)
                await session.commit()
                return True
            return False
