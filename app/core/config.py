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
    LLM_MODEL: str = "gemini-2.5-flash"
    LLM_API_BASE: str = "https://generativelanguage.googleapis.com/v1beta"
    LLM_TIMEOUT: int = 30

    # Service Configuration
    MAX_TOKENS: int = 2000
    TEMPERATURE: float = 0.7

    # RabbitMQ Configuration
    RABBITMQ_URL: str = "amqp://guest:guest@localhost/"
    RABBITMQ_QUEUE: str = "quotation.analyze"

    # Database Configuration
    DATABASE_URL: str = "postgresql://user_admin:password_123@localhost:5432/quote_analysis"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
