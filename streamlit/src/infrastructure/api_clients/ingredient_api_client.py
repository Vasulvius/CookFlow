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
