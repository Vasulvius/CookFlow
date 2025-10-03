import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Charger le fichier .env
load_dotenv()


class Settings(BaseSettings):
    """Configuration de l'application - Pattern Singleton via lru_cache."""

    model_config = SettingsConfigDict(case_sensitive=False, extra="ignore")

    # Configuration de la base de données
    database_url: str = Field(default="sqlite+aiosqlite:///./cookflow.db", description="URL de connexion à la base de données")

    # Configuration de l'application
    app_name: str = Field(default="CookFlow API", description="Nom de l'application")
    app_version: str = Field(default="0.1.0", description="Version de l'application")
    debug: bool = Field(default=False, description="Mode debug")

    # Configuration du serveur
    host: str = Field(default="127.0.0.1", description="Adresse IP du serveur")
    port: int = Field(default=8000, description="Port du serveur")

    def __init__(self, **kwargs):
        # Charger les variables d'environnement manuellement si nécessaire
        env_vars = {
            "database_url": os.getenv("DATABASE_URL"),
            "app_name": os.getenv("APP_NAME"),
            "app_version": os.getenv("APP_VERSION"),
            "debug": os.getenv("DEBUG", "").lower() in ("true", "1", "yes"),
            "host": os.getenv("HOST"),
            "port": int(os.getenv("PORT", "8000")),
        }
        # Filtrer les valeurs None
        env_vars = {k: v for k, v in env_vars.items() if v is not None}
        kwargs.update(env_vars)
        super().__init__(**kwargs)


@lru_cache()
def get_settings() -> Settings:
    """Retourne l'instance singleton des settings."""
    return Settings()
