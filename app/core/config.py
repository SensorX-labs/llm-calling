# quản lý cấu hình hệ thống
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # đọc thiết lập từ .env hoặc môi trường

    # api fastapi
    API_TITLE: str = "ai analysis service"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # kết nối 9router
    LLM_API_KEY: str = ""
    LLM_MODEL: str = "gh/gpt-4o-mini"
    LLM_API_BASE: str = "http://localhost:3001"
    LLM_TIMEOUT: int = 30

    # tham số ai
    MAX_TOKENS: int = 2000
    TEMPERATURE: float = 0.7

    # rabbitmq
    RABBITMQ_URL: str = "amqp://guest:guest@localhost/"
    RABBITMQ_QUEUE: str = "quotation.analyze"

    # postgresql
    DATABASE_URL: str = "postgresql://postgres:sk1234@localhost:5432/quote_analysis"

    class Config:
        env_file = ".env"
        case_sensitive = True


# đối tượng dùng chung toàn app
settings = Settings()
