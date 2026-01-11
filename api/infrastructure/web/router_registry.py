from fastapi import FastAPI

from api.ingredient.presentation.ingredient_router import IngredientRouter


class RouterRegistry:
    def __init__(self, app: FastAPI):
        self.routers = [IngredientRouter()]
        self._register_routers(app)

    def _register_routers(self, app: FastAPI) -> None:
        for router in self.routers:
            app.include_router(router.router)
