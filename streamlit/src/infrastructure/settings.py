import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application configuration - Singleton pattern via lru_cache."""

    def __init__(self):
        # Manually load environment variables if necessary
        self.database_url = os.getenv("DATABASE_URL")
        self.app_name = os.getenv("APP_NAME")
        self.app_version = os.getenv("APP_VERSION")
        self.debug = os.getenv("DEBUG", "").lower() in ("true", "1", "yes")
        self.host = os.getenv("HOST")
        self.port = int(os.getenv("PORT", "8000"))


@lru_cache()
def get_settings() -> Settings:
    """Returns the singleton instance of settings."""
    return Settings()
