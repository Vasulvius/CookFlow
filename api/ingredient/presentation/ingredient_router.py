from typing import List
from uuid import UUID

from fastapi import HTTPException, status

from api.infrastructure.web.abstract_router import AbstractRouter
from api.ingredient.application.ingredient_service import IngredientService
from api.ingredient.presentation.ingredient_model import (
    IngredientCreate,
    IngredientResponse,
    IngredientUpdate,
)


class IngredientRouter(AbstractRouter):
    def __init__(self):
        super().__init__(prefix="/api/ingredients", tags=["Ingredients"])
        self.service = IngredientService()

    def _register_routes(self):
        @self.router.post(
            "/",
            response_model=IngredientResponse,
            status_code=status.HTTP_201_CREATED,
            summary="Create a new ingredient",
        )
        def create_ingredient(ingredient: IngredientCreate):
            """Create a new ingredient."""
            return self.service.create_ingredient(
                name=ingredient.name, category=ingredient.category
            )

        @self.router.get(
            "/{ingredient_id}",
            response_model=IngredientResponse,
            summary="Get an ingredient by ID",
        )
        def get_ingredient(ingredient_id: UUID):
            """Get an ingredient by its ID."""
            ingredient = self.service.get_ingredient(ingredient_id)
            if not ingredient:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Ingredient with id {ingredient_id} not found",
                )
            return ingredient

        @self.router.get(
            "/", response_model=List[IngredientResponse], summary="List all ingredients"
        )
        def list_ingredients():
            """List all ingredients."""
            return self.service.list_ingredients()

        @self.router.patch(
            "/{ingredient_id}",
            response_model=IngredientResponse,
            summary="Update an ingredient",
        )
        def update_ingredient(ingredient_id: UUID, ingredient: IngredientUpdate):
            """Update an ingredient."""
            updated = self.service.update_ingredient(
                ingredient_id, name=ingredient.name, category=ingredient.category
            )
            if not updated:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Ingredient with id {ingredient_id} not found",
                )
            return updated

        @self.router.delete(
            "/{ingredient_id}",
            status_code=status.HTTP_204_NO_CONTENT,
            summary="Delete an ingredient",
        )
        def delete_ingredient(ingredient_id: UUID):
            """Delete an ingredient."""
            deleted = self.service.delete_ingredient(ingredient_id)
            if not deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Ingredient with id {ingredient_id} not found",
                )
