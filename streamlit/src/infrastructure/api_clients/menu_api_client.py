from uuid import UUID

import httpx
from src.domain.entities.menu import Menu


class MenuAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def get_menus(self) -> list[Menu]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/menus/")
            response.raise_for_status()
            data = response.json()
            return [Menu(**item) for item in data]

    async def create_menu(self, name: str, description: str, scheduled_at: str, meal_type: str, recipe_ids: list[str] = None) -> Menu:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            payload = {
                "name": name,
                "description": description,
                "scheduled_at": scheduled_at,
                "meal_type": meal_type,
                "recipe_ids": recipe_ids or [],
            }
            response = await client.post(f"{self.base_url}/menus/", json=payload)
            response.raise_for_status()
            data = response.json()
            return Menu(**data)

    async def update_menu(
        self, menu_id: UUID, name: str, description: str, scheduled_at: str, meal_type: str, recipe_ids: list[str] = None
    ) -> Menu:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            payload = {
                "name": name,
                "description": description,
                "scheduled_at": scheduled_at,
                "meal_type": meal_type,
                "recipe_ids": recipe_ids or [],
            }
            response = await client.put(f"{self.base_url}/menus/{menu_id}", json=payload)
            response.raise_for_status()
            data = response.json()
            return Menu(**data)

    async def delete_menu(self, menu_id: UUID) -> bool:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.delete(f"{self.base_url}/menus/{menu_id}")
            response.raise_for_status()
            return response.status_code == 200
