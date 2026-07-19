from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "SOAR Incident Containment Engine"
    ENV: str = "development"
    DEBUG: bool = True

    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/soar_db"
    REDIS_URL: str = "redis://localhost:6379/0"

    ABUSEIPDB_API_KEY: str = ""
    VIRUSTOTAL_API_KEY: str = ""
    GEOLITE2_DB_PATH: str = "./data/GeoLite2-City.mmdb"

    class Config:
        env_file = ".env"


settings = Settings()