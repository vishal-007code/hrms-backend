from functools import lru_cache
from pydantic import BaseSettings
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = "HRMS Lite API"
    API_V1_PREFIX: str = "/api"
    DATABASE_URL: str
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173"]

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
