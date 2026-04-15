"""Configuration module for LLM service."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # API
    API_TITLE: str = "LLM Calling Service"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # LLM Configuration
    LLM_API_KEY: str = ""
    LLM_MODEL: str = "gpt-4"
    LLM_API_BASE: str = "https://api.openai.com/v1"
    LLM_TIMEOUT: int = 30

    # Service Configuration
    MAX_TOKENS: int = 2000
    TEMPERATURE: float = 0.7

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
