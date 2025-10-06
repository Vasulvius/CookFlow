from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.domain.entities.recipe import Recipe, RecipeCreate, RecipeRead, RecipeUpdate
from src.domain.repositories.recipe_repository import RecipeRepository

router = APIRouter()
recipe_repository = RecipeRepository()


@router.post("/", response_model=RecipeRead)
async def create_recipe(recipe_create: RecipeCreate):
    """Create a new recipe."""
    try:
        recipe = Recipe.model_validate(recipe_create.model_dump())
        created_recipe = await recipe_repository.add(recipe)
        return created_recipe
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[RecipeRead])
async def read_recipes():
    """Retrieve all recipes."""
    return await recipe_repository.get_all()


@router.get("/{recipe_id}", response_model=RecipeRead)
async def read_recipe(recipe_id: UUID):
    """Retrieve a recipe by its ID."""
    recipe = await recipe_repository.get_by_id(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.put("/{recipe_id}", response_model=RecipeRead)
async def update_recipe(recipe_id: UUID, updated_recipe: RecipeUpdate):
    """Update an existing recipe."""
    existing_recipe = await recipe_repository.get_by_id(recipe_id)
    if not existing_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    updated_recipe = existing_recipe.model_copy(update=updated_recipe.model_dump(exclude_unset=True))
    try:
        result = await recipe_repository.update(updated_recipe)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{recipe_id}")
async def delete_recipe(recipe_id: UUID):
    """Delete a recipe by its ID."""
    try:
        await recipe_repository.delete(recipe_id)
        return {"detail": "Recipe successfully deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
