from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    APP_NAME: str = "SOAR Incident Containment Engine"
    ENV: str = "development"
    DEBUG: bool = True

    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/soar_db"
    REDIS_URL: str = "redis://localhost:6379/0"


settings = Settings()