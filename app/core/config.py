from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    PROJECT_NAME: str = "HRMS Lite API"
    API_V1_PREFIX: str = "/api"
    DATABASE_URL: str = "sqlite:///./hrms_lite.db"
    BACKEND_CORS_ORIGINS: str = ""


@lru_cache
def get_settings():
    return Settings()
