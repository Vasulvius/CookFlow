from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.domain.entities.ingredient import (
    Ingredient,
    IngredientCreate,
    IngredientRead,
    IngredientUpdate,
)
from src.domain.repositories.ingredient_repository import IngredientRepository

router = APIRouter()
ingredient_repository = IngredientRepository()


@router.post("/", response_model=IngredientRead)
async def create_ingredient(ingredient_create: IngredientCreate):
    """Create a new ingredient."""
    try:
        ingredient = Ingredient.model_validate(ingredient_create.model_dump())
        created_ingredient = await ingredient_repository.add(ingredient)
        return created_ingredient
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[IngredientRead])
async def read_ingredients():
    """Retrieve all ingredients."""
    return await ingredient_repository.get_all()


@router.get("/{ingredient_id}", response_model=IngredientRead)
async def read_ingredient(ingredient_id: UUID):
    """Retrieve a ingredient by its ID."""
    ingredient = await ingredient_repository.get_by_id(ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient


@router.put("/{ingredient_id}", response_model=IngredientRead)
async def update_ingredient(ingredient_id: UUID, updated_ingredient: IngredientUpdate):
    """Update an existing ingredient."""
    existing_ingredient = await ingredient_repository.get_by_id(ingredient_id)
    if not existing_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    updated_ingredient = existing_ingredient.model_copy(update=updated_ingredient.model_dump(exclude_unset=True))
    try:
        result = await ingredient_repository.update(updated_ingredient)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{ingredient_id}")
async def delete_ingredient(ingredient_id: UUID):
    """Delete an ingredient by its ID."""
    try:
        await ingredient_repository.delete(ingredient_id)
        return {"detail": "Ingredient successfully deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
