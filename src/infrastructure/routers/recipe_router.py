from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.entities.recipe import Recipe, RecipeCreate, RecipeRead, RecipeUpdate
from src.repositories.recipe_repository import RecipeRepository

router = APIRouter()
recipe_repository = RecipeRepository()


@router.post("/recipes/", response_model=RecipeRead)
async def create_recipe(recipe_create: RecipeCreate):
    """Créer une nouvelle recette."""
    try:
        recipe = Recipe.model_validate(recipe_create.model_dump())
        created_recipe = await recipe_repository.add(recipe)
        return created_recipe
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/recipes/", response_model=List[RecipeRead])
async def read_recipes():
    """Récupérer toutes les recettes."""
    return await recipe_repository.get_all()


@router.get("/recipes/{recipe_id}", response_model=RecipeRead)
async def read_recipe(recipe_id: UUID):
    """Récupérer une recette par son ID."""
    recipe = await recipe_repository.get_by_id(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recette non trouvée")
    return recipe


@router.put("/recipes/{recipe_id}", response_model=RecipeRead)
async def update_recipe(recipe_id: UUID, updated_recipe: RecipeUpdate):
    """Mettre à jour une recette existante."""
    existing_recipe = await recipe_repository.get_by_id(recipe_id)
    if not existing_recipe:
        raise HTTPException(status_code=404, detail="Recette non trouvée")
    updated_recipe = existing_recipe.model_copy(update=updated_recipe.model_dump(exclude_unset=True))
    try:
        result = await recipe_repository.update(updated_recipe)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/recipes/{recipe_id}")
async def delete_recipe(recipe_id: UUID):
    """Supprimer une recette par son ID."""
    try:
        await recipe_repository.delete(recipe_id)
        return {"detail": "Recette supprimée avec succès"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
