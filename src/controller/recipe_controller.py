from framefox.core.controller.abstract_controller import AbstractController
from framefox.core.routing.decorator.route import Route
from typing import Dict
from src.repository.recipe_repository import RecipeRepository
from src.entity.recipe import Recipe
from framefox.core.orm.entity_manager_interface import EntityManagerInterface


class RecipeController(AbstractController):
    def __init__(self, entityManager: EntityManagerInterface):
        self.entity_manager = entityManager
        self.repository = RecipeRepository()

    @Route("/recipes", "recipe.index", methods=["GET"])
    async def index(self):
        """GET /recipes - Retrieve all recipe resources"""
        try:
            items = self.repository.find_all()
            return self.json({
                "recipes": [item.dict() for item in items],
                "total": len(items),
                "status": "success"
            }, status=200)
        except Exception as e:
            return self.json({
                "error": "Failed to retrieve recipes",
                "message": str(e),
                "status": "error"
            }, status=500)

    @Route("/recipes/{id}", "recipe.show", methods=["GET"])
    async def show(self, id: int):
        """GET /recipes/{id} - Retrieve a specific recipe resource"""
        try:
            item = self.repository.find(id)
            if not item:
                return self.json({
                    "error": "Recipe not found",
                    "status": "not_found"
                }, status=404)

            return self.json({
                "recipe": item.dict(),
                "status": "success"
            }, status=200)
        except Exception as e:
            return self.json({
                "error": "Failed to retrieve recipe",
                "message": str(e),
                "status": "error"
            }, status=500)

    @Route("/recipes", "recipe.create", methods=["POST"])
    async def create(self, data: Recipe.generate_create_model()):
        """POST /recipes - Create a new recipe resource"""
        try:
            recipe = self.repository.model(**data.dict())
            self.entity_manager.persist(recipe)
            self.entity_manager.commit()

            self.entity_manager.refresh(recipe)

            return self.json({
                "recipe": recipe.dict(),
                "message": "Recipe created successfully",
                "status": "created"
            }, status=201)
        except Exception as e:
            return self.json({
                "error": "Failed to create recipe",
                "message": str(e),
                "status": "error"
            }, status=400)

    @Route("/recipes/{id}", "data.update", methods=["PUT"])
    async def update(self, id: int, data: Recipe.generate_create_model()):
        """PUT /recipes/{id} - Replace the entire recipe resource"""
        try:
            recipe = self.repository.find(id)
            if not recipe:
                return self.json({
                    "error": "Recipe not found",
                    "status": "not_found"
                }, status=404)

            # Complete replacement of the resource
            update_data = data.dict()
            for key, value in update_data.items():
                if hasattr(recipe, key):
                    setattr(recipe, key, value)

            self.entity_manager.persist(recipe)
            self.entity_manager.commit()

            self.entity_manager.refresh(recipe)

            return self.json({
                "recipe": recipe.dict(),
                "message": "Recipe updated successfully",
                "status": "updated"
            }, status=200)
        except Exception as e:
            return self.json({
                "error": "Failed to update recipe",
                "message": str(e),
                "status": "error"
            }, status=400)

    @Route("/recipes/{id}", "recipe.patch", methods=["PATCH"])
    async def patch(self, id: int, data: Recipe.generate_patch_model()):
        """PATCH /recipes/{id} - Partially update a recipe resource"""
        try:
            recipe = self.repository.find(id)
            if not recipe:
                return self.json({
                    "error": "Recipe not found",
                    "status": "not_found"
                }, status=404)

            update_data = data.dict(exclude_unset=True)

            # Partial update - only modify provided fields
            for key, value in update_data.items():
                if hasattr(recipe, key):
                    setattr(recipe, key, value)

            self.entity_manager.persist(recipe)
            self.entity_manager.commit()

            self.entity_manager.refresh(recipe)

            return self.json({
                "recipe": recipe.dict(),
                "message": "Recipe partially updated successfully",
                "status": "updated"
            }, status=200)
        except Exception as e:
            return self.json({
                "error": "Failed to patch recipe",
                "message": str(e),
                "status": "error"
            }, status=400)

    @Route("/recipes/{id}", "recipe.destroy", methods=["DELETE"])
    async def destroy(self, id: int):
        """DELETE /recipes/{id} - Delete a recipe resource"""
        try:
            recipe = self.repository.find(id)
            if not recipe:
                return self.json({
                    "error": "Recipe not found",
                    "status": "not_found"
                }, status=404)

            self.entity_manager.delete(recipe)
            self.entity_manager.commit()

            return self.json({
                "message": "Recipe deleted successfully",
                "status": "deleted"
            }, status=204)
        except Exception as e:
            return self.json({
                "error": "Failed to delete recipe",
                "message": str(e),
                "status": "error"
            }, status=500)