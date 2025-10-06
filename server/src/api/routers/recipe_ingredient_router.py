from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.domain.entities.recipe_ingredient import (
    RecipeIngredient,
    RecipeIngredientCreate,
    RecipeIngredientRead,
    RecipeIngredientUpdate,
)
from src.domain.repositories.recipe_ingredient_repository import (
    RecipeIngredientRepository,
)

router = APIRouter()

recipe_ingredient_repository = RecipeIngredientRepository()


@router.post("/", response_model=RecipeIngredientRead)
async def create_recipe_ingredient(recipe_ingredient_create: RecipeIngredientCreate):
    """Create a new recipe ingredient."""
    try:
        recipe_ingredient = RecipeIngredient.model_validate(recipe_ingredient_create.model_dump())
        created_recipe_ingredient = await recipe_ingredient_repository.add(recipe_ingredient)
        return created_recipe_ingredient
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[RecipeIngredientRead])
async def read_recipe_ingredients():
    """Retrieve all recipe ingredients."""
    return await recipe_ingredient_repository.get_all()


@router.get("/{recipe_ingredient_id}", response_model=RecipeIngredientRead)
async def read_recipe_ingredient(recipe_ingredient_id: UUID):
    """Retrieve a recipe ingredient by its ID."""
    recipe_ingredient = await recipe_ingredient_repository.get_by_id(recipe_ingredient_id)
    if not recipe_ingredient:
        raise HTTPException(status_code=404, detail="Recipe ingredient not found")
    return recipe_ingredient


@router.put("/{recipe_ingredient_id}", response_model=RecipeIngredientRead)
async def update_recipe_ingredient(recipe_ingredient_id: UUID, updated_recipe_ingredient: RecipeIngredientUpdate):
    """Update an existing recipe ingredient."""
    existing_recipe_ingredient = await recipe_ingredient_repository.get_by_id(recipe_ingredient_id)
    if not existing_recipe_ingredient:
        raise HTTPException(status_code=404, detail="Recipe ingredient not found")
    updated_recipe_ingredient = existing_recipe_ingredient.model_copy(update=updated_recipe_ingredient.model_dump(exclude_unset=True))
    try:
        result = await recipe_ingredient_repository.update(updated_recipe_ingredient)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{recipe_ingredient_id}")
async def delete_recipe_ingredient(recipe_ingredient_id: UUID):
    """Delete a recipe ingredient by its ID."""
    try:
        await recipe_ingredient_repository.delete(recipe_ingredient_id)
        return {"detail": "Recipe ingredient successfully deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
