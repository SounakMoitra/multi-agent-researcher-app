from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings, loaded from environment variables / .env file."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    openai_api_key: str
    tavily_api_key: str
    default_model_name: str = "gpt-4o-mini"
    default_temperature: float = 0.7
    cors_allow_origins: list[str] = ["*"]


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance — avoids re-reading .env on every call."""
    return Settings()