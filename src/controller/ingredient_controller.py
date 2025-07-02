from framefox.core.controller.abstract_controller import AbstractController
from framefox.core.routing.decorator.route import Route
from typing import Dict
from src.repository.ingredient_repository import IngredientRepository
from src.entity.ingredient import Ingredient
from framefox.core.orm.entity_manager_interface import EntityManagerInterface


class IngredientController(AbstractController):
    def __init__(self, entityManager: EntityManagerInterface):
        self.entity_manager = entityManager
        self.repository = IngredientRepository()

    @Route("/ingredients", "ingredient.index", methods=["GET"])
    async def index(self):
        """GET /ingredients - Retrieve all ingredient resources"""
        try:
            items = self.repository.find_all()
            return self.json({
                "ingredients": [item.dict() for item in items],
                "total": len(items),
                "status": "success"
            }, status=200)
        except Exception as e:
            return self.json({
                "error": "Failed to retrieve ingredients",
                "message": str(e),
                "status": "error"
            }, status=500)

    @Route("/ingredients/{id}", "ingredient.show", methods=["GET"])
    async def show(self, id: int):
        """GET /ingredients/{id} - Retrieve a specific ingredient resource"""
        try:
            item = self.repository.find(id)
            if not item:
                return self.json({
                    "error": "Ingredient not found",
                    "status": "not_found"
                }, status=404)

            return self.json({
                "ingredient": item.dict(),
                "status": "success"
            }, status=200)
        except Exception as e:
            return self.json({
                "error": "Failed to retrieve ingredient",
                "message": str(e),
                "status": "error"
            }, status=500)

    @Route("/ingredients", "ingredient.create", methods=["POST"])
    async def create(self, data: Ingredient.generate_create_model()):
        """POST /ingredients - Create a new ingredient resource"""
        try:
            ingredient = self.repository.model(**data.dict())
            self.entity_manager.persist(ingredient)
            self.entity_manager.commit()

            self.entity_manager.refresh(ingredient)

            return self.json({
                "ingredient": ingredient.dict(),
                "message": "Ingredient created successfully",
                "status": "created"
            }, status=201)
        except Exception as e:
            return self.json({
                "error": "Failed to create ingredient",
                "message": str(e),
                "status": "error"
            }, status=400)

    @Route("/ingredients/{id}", "data.update", methods=["PUT"])
    async def update(self, id: int, data: Ingredient.generate_create_model()):
        """PUT /ingredients/{id} - Replace the entire ingredient resource"""
        try:
            ingredient = self.repository.find(id)
            if not ingredient:
                return self.json({
                    "error": "Ingredient not found",
                    "status": "not_found"
                }, status=404)

            # Complete replacement of the resource
            update_data = data.dict()
            for key, value in update_data.items():
                if hasattr(ingredient, key):
                    setattr(ingredient, key, value)

            self.entity_manager.persist(ingredient)
            self.entity_manager.commit()

            self.entity_manager.refresh(ingredient)

            return self.json({
                "ingredient": ingredient.dict(),
                "message": "Ingredient updated successfully",
                "status": "updated"
            }, status=200)
        except Exception as e:
            return self.json({
                "error": "Failed to update ingredient",
                "message": str(e),
                "status": "error"
            }, status=400)

    @Route("/ingredients/{id}", "ingredient.patch", methods=["PATCH"])
    async def patch(self, id: int, data: Ingredient.generate_patch_model()):
        """PATCH /ingredients/{id} - Partially update a ingredient resource"""
        try:
            ingredient = self.repository.find(id)
            if not ingredient:
                return self.json({
                    "error": "Ingredient not found",
                    "status": "not_found"
                }, status=404)

            update_data = data.dict(exclude_unset=True)

            # Partial update - only modify provided fields
            for key, value in update_data.items():
                if hasattr(ingredient, key):
                    setattr(ingredient, key, value)

            self.entity_manager.persist(ingredient)
            self.entity_manager.commit()

            self.entity_manager.refresh(ingredient)

            return self.json({
                "ingredient": ingredient.dict(),
                "message": "Ingredient partially updated successfully",
                "status": "updated"
            }, status=200)
        except Exception as e:
            return self.json({
                "error": "Failed to patch ingredient",
                "message": str(e),
                "status": "error"
            }, status=400)

    @Route("/ingredients/{id}", "ingredient.destroy", methods=["DELETE"])
    async def destroy(self, id: int):
        """DELETE /ingredients/{id} - Delete a ingredient resource"""
        try:
            ingredient = self.repository.find(id)
            if not ingredient:
                return self.json({
                    "error": "Ingredient not found",
                    "status": "not_found"
                }, status=404)

            self.entity_manager.delete(ingredient)
            self.entity_manager.commit()

            return self.json({
                "message": "Ingredient deleted successfully",
                "status": "deleted"
            }, status=204)
        except Exception as e:
            return self.json({
                "error": "Failed to delete ingredient",
                "message": str(e),
                "status": "error"
            }, status=500)