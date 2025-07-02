from framefox.core.controller.abstract_controller import AbstractController
from framefox.core.routing.decorator.route import Route
from typing import Dict
from src.repository.meal_repository import MealRepository
from src.entity.meal import Meal
from framefox.core.orm.entity_manager_interface import EntityManagerInterface


class MealController(AbstractController):
    def __init__(self, entityManager: EntityManagerInterface):
        self.entity_manager = entityManager
        self.repository = MealRepository()

    @Route("/meals", "meal.index", methods=["GET"])
    async def index(self):
        """GET /meals - Retrieve all meal resources"""
        try:
            items = self.repository.find_all()
            return self.json({
                "meals": [item.dict() for item in items],
                "total": len(items),
                "status": "success"
            }, status=200)
        except Exception as e:
            return self.json({
                "error": "Failed to retrieve meals",
                "message": str(e),
                "status": "error"
            }, status=500)

    @Route("/meals/{id}", "meal.show", methods=["GET"])
    async def show(self, id: int):
        """GET /meals/{id} - Retrieve a specific meal resource"""
        try:
            item = self.repository.find(id)
            if not item:
                return self.json({
                    "error": "Meal not found",
                    "status": "not_found"
                }, status=404)

            return self.json({
                "meal": item.dict(),
                "status": "success"
            }, status=200)
        except Exception as e:
            return self.json({
                "error": "Failed to retrieve meal",
                "message": str(e),
                "status": "error"
            }, status=500)

    @Route("/meals", "meal.create", methods=["POST"])
    async def create(self, data: Meal.generate_create_model()):
        """POST /meals - Create a new meal resource"""
        try:
            meal = self.repository.model(**data.dict())
            self.entity_manager.persist(meal)
            self.entity_manager.commit()

            self.entity_manager.refresh(meal)

            return self.json({
                "meal": meal.dict(),
                "message": "Meal created successfully",
                "status": "created"
            }, status=201)
        except Exception as e:
            return self.json({
                "error": "Failed to create meal",
                "message": str(e),
                "status": "error"
            }, status=400)

    @Route("/meals/{id}", "data.update", methods=["PUT"])
    async def update(self, id: int, data: Meal.generate_create_model()):
        """PUT /meals/{id} - Replace the entire meal resource"""
        try:
            meal = self.repository.find(id)
            if not meal:
                return self.json({
                    "error": "Meal not found",
                    "status": "not_found"
                }, status=404)

            # Complete replacement of the resource
            update_data = data.dict()
            for key, value in update_data.items():
                if hasattr(meal, key):
                    setattr(meal, key, value)

            self.entity_manager.persist(meal)
            self.entity_manager.commit()

            self.entity_manager.refresh(meal)

            return self.json({
                "meal": meal.dict(),
                "message": "Meal updated successfully",
                "status": "updated"
            }, status=200)
        except Exception as e:
            return self.json({
                "error": "Failed to update meal",
                "message": str(e),
                "status": "error"
            }, status=400)

    @Route("/meals/{id}", "meal.patch", methods=["PATCH"])
    async def patch(self, id: int, data: Meal.generate_patch_model()):
        """PATCH /meals/{id} - Partially update a meal resource"""
        try:
            meal = self.repository.find(id)
            if not meal:
                return self.json({
                    "error": "Meal not found",
                    "status": "not_found"
                }, status=404)

            update_data = data.dict(exclude_unset=True)

            # Partial update - only modify provided fields
            for key, value in update_data.items():
                if hasattr(meal, key):
                    setattr(meal, key, value)

            self.entity_manager.persist(meal)
            self.entity_manager.commit()

            self.entity_manager.refresh(meal)

            return self.json({
                "meal": meal.dict(),
                "message": "Meal partially updated successfully",
                "status": "updated"
            }, status=200)
        except Exception as e:
            return self.json({
                "error": "Failed to patch meal",
                "message": str(e),
                "status": "error"
            }, status=400)

    @Route("/meals/{id}", "meal.destroy", methods=["DELETE"])
    async def destroy(self, id: int):
        """DELETE /meals/{id} - Delete a meal resource"""
        try:
            meal = self.repository.find(id)
            if not meal:
                return self.json({
                    "error": "Meal not found",
                    "status": "not_found"
                }, status=404)

            self.entity_manager.delete(meal)
            self.entity_manager.commit()

            return self.json({
                "message": "Meal deleted successfully",
                "status": "deleted"
            }, status=204)
        except Exception as e:
            return self.json({
                "error": "Failed to delete meal",
                "message": str(e),
                "status": "error"
            }, status=500)