from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # === Project Config ===
    PROJECT_NAME: str = "BOTS-ON-STRING"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = True

    # === Environment Variables ===
    OPENAI_API_KEY: str
    QDRANT_URL: str = "http://localhost:6333"
    DATABASE_URL: str = "sqlite:///./bots_on_string.db"  # or PostgreSQL URL

    # === JWT Config ===
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Cache the settings instance to avoid reloading .env repeatedly."""
    return Settings()
settings = get_settings()
