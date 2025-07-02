from framefox.core.controller.abstract_controller import AbstractController
from framefox.core.routing.decorator.route import Route
from typing import Dict
from src.repository.recipe_ingredient_repository import RecipeIngredientRepository
from src.entity.recipe_ingredient import RecipeIngredient
from framefox.core.orm.entity_manager_interface import EntityManagerInterface


class RecipeIngredientController(AbstractController):
    def __init__(self, entityManager: EntityManagerInterface):
        self.entity_manager = entityManager
        self.repository = RecipeIngredientRepository()

    @Route("/recipe_ingredients", "recipe_ingredient.index", methods=["GET"])
    async def index(self):
        """GET /recipe_ingredients - Retrieve all recipe_ingredient resources"""
        try:
            items = self.repository.find_all()
            return self.json({
                "recipe_ingredients": [item.dict() for item in items],
                "total": len(items),
                "status": "success"
            }, status=200)
        except Exception as e:
            return self.json({
                "error": "Failed to retrieve recipe_ingredients",
                "message": str(e),
                "status": "error"
            }, status=500)

    @Route("/recipe_ingredients/{id}", "recipe_ingredient.show", methods=["GET"])
    async def show(self, id: int):
        """GET /recipe_ingredients/{id} - Retrieve a specific recipe_ingredient resource"""
        try:
            item = self.repository.find(id)
            if not item:
                return self.json({
                    "error": "RecipeIngredient not found",
                    "status": "not_found"
                }, status=404)

            return self.json({
                "recipe_ingredient": item.dict(),
                "status": "success"
            }, status=200)
        except Exception as e:
            return self.json({
                "error": "Failed to retrieve recipe_ingredient",
                "message": str(e),
                "status": "error"
            }, status=500)

    @Route("/recipe_ingredients", "recipe_ingredient.create", methods=["POST"])
    async def create(self, data: RecipeIngredient.generate_create_model()):
        """POST /recipe_ingredients - Create a new recipe_ingredient resource"""
        try:
            recipe_ingredient = self.repository.model(**data.dict())
            self.entity_manager.persist(recipe_ingredient)
            self.entity_manager.commit()

            self.entity_manager.refresh(recipe_ingredient)

            return self.json({
                "recipe_ingredient": recipe_ingredient.dict(),
                "message": "RecipeIngredient created successfully",
                "status": "created"
            }, status=201)
        except Exception as e:
            return self.json({
                "error": "Failed to create recipe_ingredient",
                "message": str(e),
                "status": "error"
            }, status=400)

    @Route("/recipe_ingredients/{id}", "data.update", methods=["PUT"])
    async def update(self, id: int, data: RecipeIngredient.generate_create_model()):
        """PUT /recipe_ingredients/{id} - Replace the entire recipe_ingredient resource"""
        try:
            recipe_ingredient = self.repository.find(id)
            if not recipe_ingredient:
                return self.json({
                    "error": "RecipeIngredient not found",
                    "status": "not_found"
                }, status=404)

            # Complete replacement of the resource
            update_data = data.dict()
            for key, value in update_data.items():
                if hasattr(recipe_ingredient, key):
                    setattr(recipe_ingredient, key, value)

            self.entity_manager.persist(recipe_ingredient)
            self.entity_manager.commit()

            self.entity_manager.refresh(recipe_ingredient)

            return self.json({
                "recipe_ingredient": recipe_ingredient.dict(),
                "message": "RecipeIngredient updated successfully",
                "status": "updated"
            }, status=200)
        except Exception as e:
            return self.json({
                "error": "Failed to update recipe_ingredient",
                "message": str(e),
                "status": "error"
            }, status=400)

    @Route("/recipe_ingredients/{id}", "recipe_ingredient.patch", methods=["PATCH"])
    async def patch(self, id: int, data: RecipeIngredient.generate_patch_model()):
        """PATCH /recipe_ingredients/{id} - Partially update a recipe_ingredient resource"""
        try:
            recipe_ingredient = self.repository.find(id)
            if not recipe_ingredient:
                return self.json({
                    "error": "RecipeIngredient not found",
                    "status": "not_found"
                }, status=404)

            update_data = data.dict(exclude_unset=True)

            # Partial update - only modify provided fields
            for key, value in update_data.items():
                if hasattr(recipe_ingredient, key):
                    setattr(recipe_ingredient, key, value)

            self.entity_manager.persist(recipe_ingredient)
            self.entity_manager.commit()

            self.entity_manager.refresh(recipe_ingredient)

            return self.json({
                "recipe_ingredient": recipe_ingredient.dict(),
                "message": "RecipeIngredient partially updated successfully",
                "status": "updated"
            }, status=200)
        except Exception as e:
            return self.json({
                "error": "Failed to patch recipe_ingredient",
                "message": str(e),
                "status": "error"
            }, status=400)

    @Route("/recipe_ingredients/{id}", "recipe_ingredient.destroy", methods=["DELETE"])
    async def destroy(self, id: int):
        """DELETE /recipe_ingredients/{id} - Delete a recipe_ingredient resource"""
        try:
            recipe_ingredient = self.repository.find(id)
            if not recipe_ingredient:
                return self.json({
                    "error": "RecipeIngredient not found",
                    "status": "not_found"
                }, status=404)

            self.entity_manager.delete(recipe_ingredient)
            self.entity_manager.commit()

            return self.json({
                "message": "RecipeIngredient deleted successfully",
                "status": "deleted"
            }, status=204)
        except Exception as e:
            return self.json({
                "error": "Failed to delete recipe_ingredient",
                "message": str(e),
                "status": "error"
            }, status=500)