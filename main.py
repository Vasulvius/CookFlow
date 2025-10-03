from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config.settings import get_settings
from src.infrastructure.database import db_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestionnaire de cycle de vie de l'application."""
    # Startup
    print(f"Starting {get_settings().app_name} v{get_settings().app_version}")
    print(f"Database URL: {get_settings().database_url}")
    print(f"Debug mode: {get_settings().debug}")
    await db_manager.create_tables()
    yield
    # Shutdown
    await db_manager.engine.dispose()


app = FastAPI(title=get_settings().app_name, version=get_settings().app_version, lifespan=lifespan)


# class CreateRecipeRequest(BaseModel):
#     name: str
#     description: str


# class RecipeResponse(BaseModel):
#     id: UUID
#     name: str
#     description: str


async def get_db_session():
    """Dépendance pour obtenir une session de base de données."""
    async for session in db_manager.get_session():
        yield session


@app.get("/health")
async def health_check():
    """Vérifier l'état de l'application et des settings."""
    settings = get_settings()
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug,
        "database_url": settings.database_url.split("://")[0] + "://***",  # Masquer les credentials
    }


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=settings.debug)
