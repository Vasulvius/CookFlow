from framefox.core.controller.abstract_controller import AbstractController
from framefox.core.routing.decorator.route import Route
from typing import Dict
from src.repository.meal_recipe_repository import MealRecipeRepository
from src.entity.meal_recipe import MealRecipe
from framefox.core.orm.entity_manager_interface import EntityManagerInterface


class MealRecipeController(AbstractController):
    def __init__(self, entityManager: EntityManagerInterface):
        self.entity_manager = entityManager
        self.repository = MealRecipeRepository()

    @Route("/meal_recipes", "meal_recipe.index", methods=["GET"])
    async def index(self):
        """GET /meal_recipes - Retrieve all meal_recipe resources"""
        try:
            items = self.repository.find_all()
            return self.json({
                "meal_recipes": [item.dict() for item in items],
                "total": len(items),
                "status": "success"
            }, status=200)
        except Exception as e:
            return self.json({
                "error": "Failed to retrieve meal_recipes",
                "message": str(e),
                "status": "error"
            }, status=500)

    @Route("/meal_recipes/{id}", "meal_recipe.show", methods=["GET"])
    async def show(self, id: int):
        """GET /meal_recipes/{id} - Retrieve a specific meal_recipe resource"""
        try:
            item = self.repository.find(id)
            if not item:
                return self.json({
                    "error": "MealRecipe not found",
                    "status": "not_found"
                }, status=404)

            return self.json({
                "meal_recipe": item.dict(),
                "status": "success"
            }, status=200)
        except Exception as e:
            return self.json({
                "error": "Failed to retrieve meal_recipe",
                "message": str(e),
                "status": "error"
            }, status=500)

    @Route("/meal_recipes", "meal_recipe.create", methods=["POST"])
    async def create(self, data: MealRecipe.generate_create_model()):
        """POST /meal_recipes - Create a new meal_recipe resource"""
        try:
            meal_recipe = self.repository.model(**data.dict())
            self.entity_manager.persist(meal_recipe)
            self.entity_manager.commit()

            self.entity_manager.refresh(meal_recipe)

            return self.json({
                "meal_recipe": meal_recipe.dict(),
                "message": "MealRecipe created successfully",
                "status": "created"
            }, status=201)
        except Exception as e:
            return self.json({
                "error": "Failed to create meal_recipe",
                "message": str(e),
                "status": "error"
            }, status=400)

    @Route("/meal_recipes/{id}", "data.update", methods=["PUT"])
    async def update(self, id: int, data: MealRecipe.generate_create_model()):
        """PUT /meal_recipes/{id} - Replace the entire meal_recipe resource"""
        try:
            meal_recipe = self.repository.find(id)
            if not meal_recipe:
                return self.json({
                    "error": "MealRecipe not found",
                    "status": "not_found"
                }, status=404)

            # Complete replacement of the resource
            update_data = data.dict()
            for key, value in update_data.items():
                if hasattr(meal_recipe, key):
                    setattr(meal_recipe, key, value)

            self.entity_manager.persist(meal_recipe)
            self.entity_manager.commit()

            self.entity_manager.refresh(meal_recipe)

            return self.json({
                "meal_recipe": meal_recipe.dict(),
                "message": "MealRecipe updated successfully",
                "status": "updated"
            }, status=200)
        except Exception as e:
            return self.json({
                "error": "Failed to update meal_recipe",
                "message": str(e),
                "status": "error"
            }, status=400)

    @Route("/meal_recipes/{id}", "meal_recipe.patch", methods=["PATCH"])
    async def patch(self, id: int, data: MealRecipe.generate_patch_model()):
        """PATCH /meal_recipes/{id} - Partially update a meal_recipe resource"""
        try:
            meal_recipe = self.repository.find(id)
            if not meal_recipe:
                return self.json({
                    "error": "MealRecipe not found",
                    "status": "not_found"
                }, status=404)

            update_data = data.dict(exclude_unset=True)

            # Partial update - only modify provided fields
            for key, value in update_data.items():
                if hasattr(meal_recipe, key):
                    setattr(meal_recipe, key, value)

            self.entity_manager.persist(meal_recipe)
            self.entity_manager.commit()

            self.entity_manager.refresh(meal_recipe)

            return self.json({
                "meal_recipe": meal_recipe.dict(),
                "message": "MealRecipe partially updated successfully",
                "status": "updated"
            }, status=200)
        except Exception as e:
            return self.json({
                "error": "Failed to patch meal_recipe",
                "message": str(e),
                "status": "error"
            }, status=400)

    @Route("/meal_recipes/{id}", "meal_recipe.destroy", methods=["DELETE"])
    async def destroy(self, id: int):
        """DELETE /meal_recipes/{id} - Delete a meal_recipe resource"""
        try:
            meal_recipe = self.repository.find(id)
            if not meal_recipe:
                return self.json({
                    "error": "MealRecipe not found",
                    "status": "not_found"
                }, status=404)

            self.entity_manager.delete(meal_recipe)
            self.entity_manager.commit()

            return self.json({
                "message": "MealRecipe deleted successfully",
                "status": "deleted"
            }, status=204)
        except Exception as e:
            return self.json({
                "error": "Failed to delete meal_recipe",
                "message": str(e),
                "status": "error"
            }, status=500)