import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    """Application configuration - Singleton pattern via lru_cache."""

    model_config = SettingsConfigDict(case_sensitive=False, extra="ignore")

    # Database configuration
    database_url: str = Field(default="sqlite+aiosqlite:///./cookflow.db", description="Database connection URL")

    # Application configuration
    app_name: str = Field(default="CookFlow API", description="Application name")
    app_version: str = Field(default="0.1.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")

    # Server configuration
    host: str = Field(default="127.0.0.1", description="Server IP address")
    port: int = Field(default=8000, description="Server port")

    def __init__(self, **kwargs):
        # Manually load environment variables if necessary
        env_vars = {
            "database_url": os.getenv("DATABASE_URL"),
            "app_name": os.getenv("APP_NAME"),
            "app_version": os.getenv("APP_VERSION"),
            "debug": os.getenv("DEBUG", "").lower() in ("true", "1", "yes"),
            "host": os.getenv("HOST"),
            "port": int(os.getenv("PORT", "8000")),
        }
        # Filter out None values
        env_vars = {k: v for k, v in env_vars.items() if v is not None}
        kwargs.update(env_vars)
        super().__init__(**kwargs)


@lru_cache()
def get_settings() -> Settings:
    """Returns the singleton instance of settings."""
    return Settings()
