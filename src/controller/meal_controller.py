from fastapi import Request
from framefox.core.controller.abstract_controller import AbstractController
from framefox.core.routing.decorator.route import Route
from src.repository.meal_repository import MealRepository
from src.entity.meal import Meal
from framefox.core.orm.entity_manager_interface import EntityManagerInterface
from src.form.meal_type import MealType
from starlette.responses import HTMLResponse, RedirectResponse


class MealController(AbstractController):
    def __init__(self, entityManager: EntityManagerInterface):
        self.entity_manager = entityManager
        self.repository = MealRepository()

    @Route("/meals", "meal.read_all", methods=["GET"])
    async def read_all(self) -> HTMLResponse:
        items = self.repository.find_all()
        return self.render("meal/index.html", {"items": items})

    @Route("/meal/create", "meal.create", methods=["GET", "POST"])
    async def create(self, request: Request) -> HTMLResponse:
        meal = Meal()
        form = self.create_form(MealType, meal)
        await form.handle_request(request)
        if form.is_submitted() and form.is_valid():
            self.entity_manager.persist(meal)
            self.entity_manager.commit()
            self.flash("success", "Meal created successfully!")
            return self.redirect(self.generate_url("meal.read_all"))
        return self.render("meal/create.html", {
            "form": form.create_view()
        })

    @Route("/meal/{id}", "meal.read", methods=["GET"])
    async def read(self, id: int) -> HTMLResponse:
        item = self.repository.find(id)
        if not item:
            self.flash("error", "Meal not found!")
            return self.redirect(self.generate_url("meal.read_all"))
        return self.render("meal/read.html", {"item": item})

    @Route("/meal/{id}/update", "meal.update", methods=["GET", "POST"])
    async def update(self, request: Request, id: int) -> HTMLResponse:
        meal = self.repository.find(id)
        form = self.create_form(MealType, meal)

        await form.handle_request(request)
        if form.is_submitted() and form.is_valid():
            self.entity_manager.persist(meal)
            self.entity_manager.commit()
            self.flash("success", "Meal updated successfully!")
            return self.redirect(self.generate_url("meal.read_all"))

        return self.render("meal/update.html", {
            "form": form.create_view(),
            "item": meal 
        })

    @Route("/meal/delete/{id}", "meal.delete", methods=["POST"])
    async def delete(self, id: int) -> RedirectResponse:
        try:
            meal = self.repository.find(id)
            if not meal:
                self.flash("error", "Meal not found!")
                return self.redirect(self.generate_url("meal.read_all"))
            self.entity_manager.delete(meal)
            self.entity_manager.commit()
            self.flash("success", "Meal deleted successfully!")
            return self.redirect(self.generate_url("meal.read_all"))
        except Exception as e:
            self.flash("error", str(e))
            return self.redirect(self.generate_url("meal.read_all"))