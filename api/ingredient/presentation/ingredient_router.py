from api.infrastructure.web.abstract_router import AbstractRouter


class IngredientRouter(AbstractRouter):
    def __init__(self):
        super().__init__(prefix="/ingredient", tags=["Ingredients"])

    def _register_routes(self):
        @self.router.post("/")
        def create_ingredient(name: str, category: str):
            # Logic to create an ingredient
            return {"message": f"Ingredient '{name}' in category '{category}' created."}

        @self.router.get("/{ingredient_id}")
        def read_ingredient(ingredient_id: int):
            # Logic to get an ingredient by ID
            return {
                "ingredient_id": ingredient_id,
                "name": "Sample Ingredient",
                "category": "Sample Category",
            }

        @self.router.get("/")
        def list_ingredients():
            # Logic to list all ingredients
            return [{"id": 1, "name": "Sample Ingredient", "category": "Sample Category"}]
