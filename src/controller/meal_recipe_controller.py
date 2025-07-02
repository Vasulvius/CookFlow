from fastapi import Request
from framefox.core.controller.abstract_controller import AbstractController
from framefox.core.routing.decorator.route import Route
from src.repository.meal_recipe_repository import MealRecipeRepository
from src.entity.meal_recipe import MealRecipe
from framefox.core.orm.entity_manager_interface import EntityManagerInterface
from src.form.meal_recipe_type import MealRecipeType
from starlette.responses import HTMLResponse, RedirectResponse


class MealRecipeController(AbstractController):
    def __init__(self, entityManager: EntityManagerInterface):
        self.entity_manager = entityManager
        self.repository = MealRecipeRepository()

    @Route("/meal_recipes", "meal_recipe.read_all", methods=["GET"])
    async def read_all(self) -> HTMLResponse:
        items = self.repository.find_all()
        return self.render("meal_recipe/index.html", {"items": items})

    @Route("/meal_recipe/create", "meal_recipe.create", methods=["GET", "POST"])
    async def create(self, request: Request) -> HTMLResponse:
        meal_recipe = MealRecipe()
        form = self.create_form(MealRecipeType, meal_recipe)
        await form.handle_request(request)
        if form.is_submitted() and form.is_valid():
            self.entity_manager.persist(meal_recipe)
            self.entity_manager.commit()
            self.flash("success", "MealRecipe created successfully!")
            return self.redirect(self.generate_url("meal_recipe.read_all"))
        return self.render("meal_recipe/create.html", {
            "form": form.create_view()
        })

    @Route("/meal_recipe/{id}", "meal_recipe.read", methods=["GET"])
    async def read(self, id: int) -> HTMLResponse:
        item = self.repository.find(id)
        if not item:
            self.flash("error", "MealRecipe not found!")
            return self.redirect(self.generate_url("meal_recipe.read_all"))
        return self.render("meal_recipe/read.html", {"item": item})

    @Route("/meal_recipe/{id}/update", "meal_recipe.update", methods=["GET", "POST"])
    async def update(self, request: Request, id: int) -> HTMLResponse:
        meal_recipe = self.repository.find(id)
        form = self.create_form(MealRecipeType, meal_recipe)

        await form.handle_request(request)
        if form.is_submitted() and form.is_valid():
            self.entity_manager.persist(meal_recipe)
            self.entity_manager.commit()
            self.flash("success", "MealRecipe updated successfully!")
            return self.redirect(self.generate_url("meal_recipe.read_all"))

        return self.render("meal_recipe/update.html", {
            "form": form.create_view(),
            "item": meal_recipe 
        })

    @Route("/meal_recipe/delete/{id}", "meal_recipe.delete", methods=["POST"])
    async def delete(self, id: int) -> RedirectResponse:
        try:
            meal_recipe = self.repository.find(id)
            if not meal_recipe:
                self.flash("error", "MealRecipe not found!")
                return self.redirect(self.generate_url("meal_recipe.read_all"))
            self.entity_manager.delete(meal_recipe)
            self.entity_manager.commit()
            self.flash("success", "MealRecipe deleted successfully!")
            return self.redirect(self.generate_url("meal_recipe.read_all"))
        except Exception as e:
            self.flash("error", str(e))
            return self.redirect(self.generate_url("meal_recipe.read_all"))