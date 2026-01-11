from fastapi import FastAPI

from api.ingredient.presentation.ingredient_router import IngredientRouter
from api.presentation.general_router import GeneralRouter


class RouterRegistry:
    def __init__(self, app: FastAPI):
        self.routers = [IngredientRouter(), GeneralRouter()]
        self._register_routers(app)

    def _register_routers(self, app: FastAPI) -> None:
        for router in self.routers:
            app.include_router(router.router)
