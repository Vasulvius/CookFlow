from fastapi import Request
from framefox.core.controller.abstract_controller import AbstractController
from framefox.core.routing.decorator.route import Route
from starlette.responses import HTMLResponse

from src.repository.ingredient_repository import IngredientRepository
from src.repository.meal_repository import MealRepository
from src.repository.recipe_ingredient_repository import RecipeIngredientRepository
from src.repository.recipe_repository import RecipeRepository


class DashboardController(AbstractController):
    def __init__(self):
        self.ingredient_repository = IngredientRepository()
        self.recipe_repository = RecipeRepository()
        self.meal_repository = MealRepository()
        self.recipe_ingredient_repository = RecipeIngredientRepository()

    @Route("/", "dashboard.home", methods=["GET"])
    async def home(self) -> HTMLResponse:
        # Récupérer des statistiques pour le dashboard
        total_ingredients = len(self.ingredient_repository.find_all())
        total_recipes = len(self.recipe_repository.find_all())
        total_meals = len(self.meal_repository.find_all())

        # Récupérer les derniers éléments ajoutés
        recent_recipes = self.recipe_repository.find_all()[-5:] if total_recipes > 0 else []
        recent_ingredients = self.ingredient_repository.find_all()[-5:] if total_ingredients > 0 else []

        return self.render(
            "dashboard/home.html",
            {
                "total_ingredients": total_ingredients,
                "total_recipes": total_recipes,
                "total_meals": total_meals,
                "recent_recipes": recent_recipes,
                "recent_ingredients": recent_ingredients,
            },
        )
