from fastapi import Request
from framefox.core.controller.abstract_controller import AbstractController
from framefox.core.orm.entity_manager_interface import EntityManagerInterface
from framefox.core.routing.decorator.route import Route
from starlette.responses import HTMLResponse, RedirectResponse

from src.entity.recipe import Recipe
from src.entity.recipe_ingredient import RecipeIngredient
from src.form.recipe_type import RecipeType
from src.repository.ingredient_repository import IngredientRepository
from src.repository.recipe_ingredient_repository import RecipeIngredientRepository
from src.repository.recipe_repository import RecipeRepository


class RecipeController(AbstractController):
    def __init__(self, entityManager: EntityManagerInterface):
        self.entity_manager = entityManager
        self.repository = RecipeRepository()
        self.ingredient_repository = IngredientRepository()
        self.recipe_ingredient_repository = RecipeIngredientRepository()

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
        return self.render("recipe/create.html", {"form": form.create_view()})

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

        return self.render("recipe/update.html", {"form": form.create_view(), "item": recipe})

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

    @Route("/recipe/create-with-ingredients", "recipe.create_with_ingredients", methods=["GET", "POST"])
    async def create_with_ingredients(self, request: Request) -> HTMLResponse:
        recipe = Recipe()
        form = self.create_form(RecipeType, recipe)

        # Récupérer tous les ingrédients disponibles
        available_ingredients = self.ingredient_repository.find_all()

        if request.method == "POST":
            await form.handle_request(request)
            if form.is_submitted() and form.is_valid():
                # Sauvegarder la recette d'abord
                self.entity_manager.persist(recipe)
                self.entity_manager.commit()

                # Rediriger vers la page d'ajout d'ingrédients
                self.flash("success", f"Recette '{recipe.name}' créée avec succès ! Ajoutez maintenant les ingrédients.")
                return self.redirect(self.generate_url("recipe.manage_ingredients", id=recipe.id))

        return self.render(
            "recipe/create_with_ingredients.html", {"form": form.create_view(), "available_ingredients": available_ingredients}
        )

    @Route("/recipe/{id}/manage-ingredients", "recipe.manage_ingredients", methods=["GET", "POST"])
    async def manage_ingredients(self, request: Request, id: int) -> HTMLResponse:
        recipe = self.repository.find(id)
        if not recipe:
            self.flash("error", "Recette non trouvée !")
            return self.redirect(self.generate_url("recipe.read_all"))

        # Récupérer les ingrédients de la recette et tous les ingrédients disponibles
        recipe_ingredients = self.recipe_ingredient_repository.find_by({"recipe_id": id})
        available_ingredients = self.ingredient_repository.find_all()

        if request.method == "POST":
            form_data = await request.form()

            # Traitement pour ajouter un nouvel ingrédient
            if "add_ingredient" in form_data:
                ingredient_id = int(form_data.get("ingredient_id"))
                quantity = float(form_data.get("quantity"))
                unit = form_data.get("unit")

                # Vérifier si l'ingrédient n'est pas déjà dans la recette
                existing = self.recipe_ingredient_repository.find_by({"recipe_id": id, "ingredient_id": ingredient_id})

                if not existing:
                    recipe_ingredient = RecipeIngredient()
                    recipe_ingredient.recipe_id = id
                    recipe_ingredient.ingredient_id = ingredient_id
                    recipe_ingredient.quantity = quantity
                    recipe_ingredient.unit = unit

                    self.entity_manager.persist(recipe_ingredient)
                    self.entity_manager.commit()
                    self.flash("success", "Ingrédient ajouté à la recette !")
                else:
                    self.flash("warning", "Cet ingrédient est déjà dans la recette !")

                return self.redirect(self.generate_url("recipe.manage_ingredients", id=id))

            # Traitement pour modifier un ingrédient existant
            elif "update_ingredient" in form_data:
                recipe_ingredient_id = int(form_data.get("recipe_ingredient_id"))
                quantity = float(form_data.get("quantity"))
                unit = form_data.get("unit")

                recipe_ingredient = self.recipe_ingredient_repository.find(recipe_ingredient_id)
                if recipe_ingredient:
                    recipe_ingredient.quantity = quantity
                    recipe_ingredient.unit = unit
                    self.entity_manager.persist(recipe_ingredient)
                    self.entity_manager.commit()
                    self.flash("success", "Ingrédient modifié !")

                return self.redirect(self.generate_url("recipe.manage_ingredients", id=id))

            # Traitement pour supprimer un ingrédient
            elif "remove_ingredient" in form_data:
                recipe_ingredient_id = int(form_data.get("recipe_ingredient_id"))
                recipe_ingredient = self.recipe_ingredient_repository.find(recipe_ingredient_id)
                if recipe_ingredient:
                    self.entity_manager.delete(recipe_ingredient)
                    self.entity_manager.commit()
                    self.flash("success", "Ingrédient retiré de la recette !")

                return self.redirect(self.generate_url("recipe.manage_ingredients", id=id))

        return self.render(
            "recipe/manage_ingredients.html",
            {"recipe": recipe, "recipe_ingredients": recipe_ingredients, "available_ingredients": available_ingredients},
        )
