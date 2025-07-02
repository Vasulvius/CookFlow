from fastapi import Request
from framefox.core.controller.abstract_controller import AbstractController
from framefox.core.routing.decorator.route import Route
from src.repository.recipe_ingredient_repository import RecipeIngredientRepository
from src.entity.recipe_ingredient import RecipeIngredient
from framefox.core.orm.entity_manager_interface import EntityManagerInterface
from src.form.recipe_ingredient_type import RecipeIngredientType
from starlette.responses import HTMLResponse, RedirectResponse


class RecipeIngredientController(AbstractController):
    def __init__(self, entityManager: EntityManagerInterface):
        self.entity_manager = entityManager
        self.repository = RecipeIngredientRepository()

    @Route("/recipe_ingredients", "recipe_ingredient.read_all", methods=["GET"])
    async def read_all(self) -> HTMLResponse:
        items = self.repository.find_all()
        return self.render("recipe_ingredient/index.html", {"items": items})

    @Route("/recipe_ingredient/create", "recipe_ingredient.create", methods=["GET", "POST"])
    async def create(self, request: Request) -> HTMLResponse:
        recipe_ingredient = RecipeIngredient()
        form = self.create_form(RecipeIngredientType, recipe_ingredient)
        await form.handle_request(request)
        if form.is_submitted() and form.is_valid():
            self.entity_manager.persist(recipe_ingredient)
            self.entity_manager.commit()
            self.flash("success", "RecipeIngredient created successfully!")
            return self.redirect(self.generate_url("recipe_ingredient.read_all"))
        return self.render("recipe_ingredient/create.html", {
            "form": form.create_view()
        })

    @Route("/recipe_ingredient/{id}", "recipe_ingredient.read", methods=["GET"])
    async def read(self, id: int) -> HTMLResponse:
        item = self.repository.find(id)
        if not item:
            self.flash("error", "RecipeIngredient not found!")
            return self.redirect(self.generate_url("recipe_ingredient.read_all"))
        return self.render("recipe_ingredient/read.html", {"item": item})

    @Route("/recipe_ingredient/{id}/update", "recipe_ingredient.update", methods=["GET", "POST"])
    async def update(self, request: Request, id: int) -> HTMLResponse:
        recipe_ingredient = self.repository.find(id)
        form = self.create_form(RecipeIngredientType, recipe_ingredient)

        await form.handle_request(request)
        if form.is_submitted() and form.is_valid():
            self.entity_manager.persist(recipe_ingredient)
            self.entity_manager.commit()
            self.flash("success", "RecipeIngredient updated successfully!")
            return self.redirect(self.generate_url("recipe_ingredient.read_all"))

        return self.render("recipe_ingredient/update.html", {
            "form": form.create_view(),
            "item": recipe_ingredient 
        })

    @Route("/recipe_ingredient/delete/{id}", "recipe_ingredient.delete", methods=["POST"])
    async def delete(self, id: int) -> RedirectResponse:
        try:
            recipe_ingredient = self.repository.find(id)
            if not recipe_ingredient:
                self.flash("error", "RecipeIngredient not found!")
                return self.redirect(self.generate_url("recipe_ingredient.read_all"))
            self.entity_manager.delete(recipe_ingredient)
            self.entity_manager.commit()
            self.flash("success", "RecipeIngredient deleted successfully!")
            return self.redirect(self.generate_url("recipe_ingredient.read_all"))
        except Exception as e:
            self.flash("error", str(e))
            return self.redirect(self.generate_url("recipe_ingredient.read_all"))