from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    # Pydantic settings configuration
    model_config = SettingsConfigDict(env_file=".env")

    # Core app settings
    APP_NAME: str = "SOAR Incident Containment Engine"
    ENV: str = "development"
    DEBUG: bool = True

    # Database and cache
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/soar_db"
    REDIS_URL: str = "redis://localhost:6379/0"

    # Threat Intelligence API keys
    ABUSEIPDB_API_KEY: str = ""
    VIRUSTOTAL_API_KEY: str = ""

    # Path to GeoLite2 database file
    GEOLITE2_DB_PATH: str = "./data/GeoLite2-City.mmdb"


# Instantiate settings object
settings = Settings()
