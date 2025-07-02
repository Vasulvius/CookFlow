from fastapi import Request
from framefox.core.controller.abstract_controller import AbstractController
from framefox.core.routing.decorator.route import Route
from src.repository.ingredient_repository import IngredientRepository
from src.entity.ingredient import Ingredient
from framefox.core.orm.entity_manager_interface import EntityManagerInterface
from src.form.ingredient_type import IngredientType
from starlette.responses import HTMLResponse, RedirectResponse


class IngredientController(AbstractController):
    def __init__(self, entityManager: EntityManagerInterface):
        self.entity_manager = entityManager
        self.repository = IngredientRepository()

    @Route("/ingredients", "ingredient.read_all", methods=["GET"])
    async def read_all(self) -> HTMLResponse:
        items = self.repository.find_all()
        return self.render("ingredient/index.html", {"items": items})

    @Route("/ingredient/create", "ingredient.create", methods=["GET", "POST"])
    async def create(self, request: Request) -> HTMLResponse:
        ingredient = Ingredient()
        form = self.create_form(IngredientType, ingredient)
        await form.handle_request(request)
        if form.is_submitted() and form.is_valid():
            self.entity_manager.persist(ingredient)
            self.entity_manager.commit()
            self.flash("success", "Ingredient created successfully!")
            return self.redirect(self.generate_url("ingredient.read_all"))
        return self.render("ingredient/create.html", {
            "form": form.create_view()
        })

    @Route("/ingredient/{id}", "ingredient.read", methods=["GET"])
    async def read(self, id: int) -> HTMLResponse:
        item = self.repository.find(id)
        if not item:
            self.flash("error", "Ingredient not found!")
            return self.redirect(self.generate_url("ingredient.read_all"))
        return self.render("ingredient/read.html", {"item": item})

    @Route("/ingredient/{id}/update", "ingredient.update", methods=["GET", "POST"])
    async def update(self, request: Request, id: int) -> HTMLResponse:
        ingredient = self.repository.find(id)
        form = self.create_form(IngredientType, ingredient)

        await form.handle_request(request)
        if form.is_submitted() and form.is_valid():
            self.entity_manager.persist(ingredient)
            self.entity_manager.commit()
            self.flash("success", "Ingredient updated successfully!")
            return self.redirect(self.generate_url("ingredient.read_all"))

        return self.render("ingredient/update.html", {
            "form": form.create_view(),
            "item": ingredient 
        })

    @Route("/ingredient/delete/{id}", "ingredient.delete", methods=["POST"])
    async def delete(self, id: int) -> RedirectResponse:
        try:
            ingredient = self.repository.find(id)
            if not ingredient:
                self.flash("error", "Ingredient not found!")
                return self.redirect(self.generate_url("ingredient.read_all"))
            self.entity_manager.delete(ingredient)
            self.entity_manager.commit()
            self.flash("success", "Ingredient deleted successfully!")
            return self.redirect(self.generate_url("ingredient.read_all"))
        except Exception as e:
            self.flash("error", str(e))
            return self.redirect(self.generate_url("ingredient.read_all"))