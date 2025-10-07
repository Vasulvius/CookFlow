from uuid import UUID

import httpx
from src.domain.entities.recipe import Recipe


class RecipeAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def get_recipes(self) -> list[Recipe]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/recipes/")
            response.raise_for_status()
            data = response.json()
            return [Recipe(**item) for item in data]

    async def create_recipe(self, name: str, description: str) -> Recipe:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            payload = {"name": name, "description": description}
            response = await client.post(f"{self.base_url}/recipes/", json=payload)
            response.raise_for_status()
            data = response.json()
            return Recipe(**data)

    async def update_recipe(self, recipe_id: UUID, name: str, description: str) -> Recipe:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            payload = {"name": name, "description": description}
            response = await client.put(f"{self.base_url}/recipes/{recipe_id}", json=payload)
            response.raise_for_status()
            data = response.json()
            return Recipe(**data)

    async def delete_recipe(self, recipe_id: UUID) -> bool:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.delete(f"{self.base_url}/recipes/{recipe_id}")
            response.raise_for_status()
            return response.status_code == 200
