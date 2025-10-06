from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.routers import menu_router, recipe_router
from src.infrastructure import db_manager, get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle manager."""
    # Startup
    print(f"Starting {get_settings().app_name} v{get_settings().app_version}")
    print(f"Database URL: {get_settings().database_url}")
    print(f"Debug mode: {get_settings().debug}")
    await db_manager.create_tables()
    yield
    # Shutdown
    await db_manager.engine.dispose()


app = FastAPI(title=get_settings().app_name, version=get_settings().app_version, lifespan=lifespan)

app.include_router(recipe_router, prefix="/recipes", tags=["Recipes"])
app.include_router(menu_router, prefix="/menus", tags=["Menus"])


async def get_db_session():
    """Dependency to obtain a database session."""
    async for session in db_manager.get_session():
        yield session


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
