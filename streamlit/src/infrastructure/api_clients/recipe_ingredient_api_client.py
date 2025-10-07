from uuid import UUID

import httpx
from src.domain.entities.recipe_ingredient import RecipeIngredient


class RecipeIngredientAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def get_recipe_ingredients(self) -> list[RecipeIngredient]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/recipe-ingredients/")
            response.raise_for_status()
            data = response.json()
            return [RecipeIngredient(**item) for item in data]

    async def get_recipe_ingredients_by_recipe_id(self, recipe_id: UUID) -> list[RecipeIngredient]:
        """Get all ingredients for a specific recipe."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/recipe-ingredients/")
            response.raise_for_status()
            data = response.json()
            recipe_ingredients = [RecipeIngredient(**item) for item in data]
            return [ri for ri in recipe_ingredients if ri.recipe_id == recipe_id]

    async def create_recipe_ingredient(self, recipe_id: UUID, ingredient_id: UUID, quantity: float, unit: str) -> RecipeIngredient:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            payload = {"recipe_id": str(recipe_id), "ingredient_id": str(ingredient_id), "quantity": quantity, "unit": unit}
            response = await client.post(f"{self.base_url}/recipe-ingredients/", json=payload)
            response.raise_for_status()
            data = response.json()
            return RecipeIngredient(**data)

    async def update_recipe_ingredient(self, recipe_ingredient_id: UUID, quantity: float, unit: str) -> RecipeIngredient:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            payload = {"quantity": quantity, "unit": unit}
            response = await client.put(f"{self.base_url}/recipe-ingredients/{recipe_ingredient_id}", json=payload)
            response.raise_for_status()
            data = response.json()
            return RecipeIngredient(**data)

    async def delete_recipe_ingredient(self, recipe_ingredient_id: UUID) -> bool:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.delete(f"{self.base_url}/recipe-ingredients/{recipe_ingredient_id}")
            response.raise_for_status()
            return response.status_code == 200

    async def delete_all_for_recipe(self, recipe_id: UUID) -> bool:
        """Delete all recipe ingredients for a specific recipe."""
        recipe_ingredients = await self.get_recipe_ingredients_by_recipe_id(recipe_id)
        for ri in recipe_ingredients:
            await self.delete_recipe_ingredient(ri.id)
        return True
