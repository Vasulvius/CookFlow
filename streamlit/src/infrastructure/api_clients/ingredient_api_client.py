from uuid import UUID

import httpx
from src.domain.entities.ingredient import Ingredient


class IngredientAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def get_ingredients(self) -> list[Ingredient]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/ingredients/")
            response.raise_for_status()
            data = response.json()
            return [Ingredient(**item) for item in data]

    async def create_ingredient(self, name: str, description: str) -> Ingredient:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            payload = {"name": name, "description": description}
            response = await client.post(f"{self.base_url}/ingredients/", json=payload)
            response.raise_for_status()
            data = response.json()
            return Ingredient(**data)

    async def update_ingredient(self, ingredient_id: UUID, name: str, description: str) -> Ingredient:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            payload = {"name": name, "description": description}
            response = await client.put(f"{self.base_url}/ingredients/{ingredient_id}", json=payload)
            response.raise_for_status()
            data = response.json()
            return Ingredient(**data)

    async def delete_ingredient(self, ingredient_id: UUID) -> bool:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.delete(f"{self.base_url}/ingredients/{ingredient_id}")
            response.raise_for_status()
            return response.status_code == 200
