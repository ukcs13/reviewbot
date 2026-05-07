from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings and configuration.
    Loads from environment variables or .env file.
    """
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # AI
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o"

    # Database
    DATABASE_URL: str  # must start with postgresql+asyncpg://

    # Redis
    REDIS_URL: str  # must start with redis://

    # App
    FRONTEND_URL: str = "http://localhost:3000"
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    LOG_LEVEL: str = "INFO"
    MAX_ZIP_SIZE_MB: int = 50
    MAX_FILES_PER_REVIEW: int = 30
    MAX_FILE_SIZE_KB: int = 100
    REVIEW_TIMEOUT_SECONDS: int = 30

    # GitHub OAuth (for NextAuth — backend validates tokens)
    GITHUB_CLIENT_ID: str
    GITHUB_CLIENT_SECRET: str

    @property
    def is_production(self) -> bool:
        """Check if the current environment is production."""
        return self.ENVIRONMENT == "production"

    @property
    def max_zip_bytes(self) -> int:
        """Convert max zip size from MB to bytes."""
        return self.MAX_ZIP_SIZE_MB * 1024 * 1024

@lru_cache
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Uses lru_cache to avoid reloading from environment on every call.
    """
    return Settings()
