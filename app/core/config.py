from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_TITLE: str = "ai analysis service"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = False

    LLM_API_KEY: str = ""
    LLM_MODEL: str = "gh/gpt-4o-mini"
    LLM_API_BASE: str = "http://9router:20128"
    LLM_TIMEOUT: int = 30

    MAX_TOKENS: int = 2000
    TEMPERATURE: float = 0.7

    RABBITMQ_URL: str = "amqp://guest:guest@rabbitmq:5672/"
    RABBITMQ_QUEUE: str = "quotation.analyze"

    DATABASE_URL: str = "postgresql://postgres:sk1234@db:5432/quote_analysis"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


settings = Settings()
