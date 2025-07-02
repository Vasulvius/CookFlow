from fastapi import Request
from framefox.core.controller.abstract_controller import AbstractController
from framefox.core.routing.decorator.route import Route
from src.repository.recipe_repository import RecipeRepository
from src.entity.recipe import Recipe
from framefox.core.orm.entity_manager_interface import EntityManagerInterface
from src.form.recipe_type import RecipeType
from starlette.responses import HTMLResponse, RedirectResponse


class RecipeController(AbstractController):
    def __init__(self, entityManager: EntityManagerInterface):
        self.entity_manager = entityManager
        self.repository = RecipeRepository()

    @Route("/recipes", "recipe.read_all", methods=["GET"])
    async def read_all(self) -> HTMLResponse:
        items = self.repository.find_all()
        return self.render("recipe/index.html", {"items": items})

    @Route("/recipe/create", "recipe.create", methods=["GET", "POST"])
    async def create(self, request: Request) -> HTMLResponse:
        recipe = Recipe()
        form = self.create_form(RecipeType, recipe)
        await form.handle_request(request)
        if form.is_submitted() and form.is_valid():
            self.entity_manager.persist(recipe)
            self.entity_manager.commit()
            self.flash("success", "Recipe created successfully!")
            return self.redirect(self.generate_url("recipe.read_all"))
        return self.render("recipe/create.html", {
            "form": form.create_view()
        })

    @Route("/recipe/{id}", "recipe.read", methods=["GET"])
    async def read(self, id: int) -> HTMLResponse:
        item = self.repository.find(id)
        if not item:
            self.flash("error", "Recipe not found!")
            return self.redirect(self.generate_url("recipe.read_all"))
        return self.render("recipe/read.html", {"item": item})

    @Route("/recipe/{id}/update", "recipe.update", methods=["GET", "POST"])
    async def update(self, request: Request, id: int) -> HTMLResponse:
        recipe = self.repository.find(id)
        form = self.create_form(RecipeType, recipe)

        await form.handle_request(request)
        if form.is_submitted() and form.is_valid():
            self.entity_manager.persist(recipe)
            self.entity_manager.commit()
            self.flash("success", "Recipe updated successfully!")
            return self.redirect(self.generate_url("recipe.read_all"))

        return self.render("recipe/update.html", {
            "form": form.create_view(),
            "item": recipe 
        })

    @Route("/recipe/delete/{id}", "recipe.delete", methods=["POST"])
    async def delete(self, id: int) -> RedirectResponse:
        try:
            recipe = self.repository.find(id)
            if not recipe:
                self.flash("error", "Recipe not found!")
                return self.redirect(self.generate_url("recipe.read_all"))
            self.entity_manager.delete(recipe)
            self.entity_manager.commit()
            self.flash("success", "Recipe deleted successfully!")
            return self.redirect(self.generate_url("recipe.read_all"))
        except Exception as e:
            self.flash("error", str(e))
            return self.redirect(self.generate_url("recipe.read_all"))