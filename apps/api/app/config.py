from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_port: int = 8000
    api_host: str = "0.0.0.0"
    cors_origins: str = "http://localhost:3000"
    database_url: str = "postgresql+asyncpg://ai_interviewer:ai_interviewer@localhost:5432/ai_interviewer"
    database_url_sync: str = (
        "postgresql+psycopg2://ai_interviewer:ai_interviewer@localhost:5432/ai_interviewer"
    )

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
