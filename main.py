from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.routers import (
    ingredient_router,
    menu_router,
    recipe_ingredient_router,
    recipe_router,
)
from src.infrastructure import db_manager, get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle manager."""
    # Startup
    await db_manager.create_tables()

    # Rebuild Pydantic models to resolve forward references
    from src.domain.entities.ingredient import (
        Ingredient,
        IngredientCreate,
        IngredientRead,
        IngredientUpdate,
    )
    from src.domain.entities.recipe import (
        Recipe,
        RecipeCreate,
        RecipeRead,
        RecipeUpdate,
    )
    from src.domain.entities.recipe_ingredient import (
        RecipeIngredient,
        RecipeIngredientCreate,
        RecipeIngredientRead,
        RecipeIngredientUpdate,
    )

    # Rebuild all models
    Recipe.model_rebuild()
    RecipeCreate.model_rebuild()
    RecipeRead.model_rebuild()
    RecipeUpdate.model_rebuild()

    Ingredient.model_rebuild()
    IngredientCreate.model_rebuild()
    IngredientRead.model_rebuild()
    IngredientUpdate.model_rebuild()

    RecipeIngredient.model_rebuild()
    RecipeIngredientCreate.model_rebuild()
    RecipeIngredientRead.model_rebuild()
    RecipeIngredientUpdate.model_rebuild()

    yield
    # Shutdown
    await db_manager.engine.dispose()


app = FastAPI(title=get_settings().app_name, version=get_settings().app_version, lifespan=lifespan)

app.include_router(recipe_router, prefix="/recipes", tags=["Recipes"])
app.include_router(menu_router, prefix="/menus", tags=["Menus"])
app.include_router(ingredient_router, prefix="/ingredients", tags=["Ingredients"])
app.include_router(recipe_ingredient_router, prefix="/recipe-ingredients", tags=["Recipe Ingredients"])


@app.get("/health")
async def health_check():
    """Check the application's status and settings."""
    settings = get_settings()
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug,
    }


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=settings.debug)
