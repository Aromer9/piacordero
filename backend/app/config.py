from pydantic_settings import BaseSettings
from motor.motor_asyncio import AsyncIOMotorClient
from functools import lru_cache


class Settings(BaseSettings):
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db: str = "piacordero"
    upload_dir: str = "uploads"
    allowed_origins: str = "http://localhost:5173"
    admin_password: str = "piacordero2024"
    secret_key: str = "changeme-use-a-long-random-string-in-production"
    token_expire_hours: int = 72

    class Config:
        env_file = ".env"

    @property
    def origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",")]


@lru_cache
def get_settings() -> Settings:
    return Settings()


_client: AsyncIOMotorClient | None = None


def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        settings = get_settings()
        _client = AsyncIOMotorClient(settings.mongodb_uri)
    return _client


def get_db():
    settings = get_settings()
    return get_client()[settings.mongodb_db]
