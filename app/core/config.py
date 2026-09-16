"""Конфигурация приложения: читаем переменные окружения из .env."""

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    secret_key: str
    database_url: str
    access_token_expire_minutes: int = 30
    jwt_algorithm: str = "HS256"

    # Префикс для всех маршрутов текущей версии API
    api_v1_prefix: str = "/api/v1"

    # Кому разрешено обращаться из браузера (через запятую)
    cors_origins: str = "http://localhost:3000,http://localhost:5173"

    @field_validator("secret_key")
    @classmethod
    def secret_must_be_real(cls, value: str) -> str:
        """Защита от деплоя с секретом-заглушкой."""
        if value in ("", "change-me"):
            raise ValueError("Заполни SECRET_KEY в файле .env")
        return value

    @property
    def cors_origins_list(self) -> list[str]:
        """Строка из .env → список источников."""
        return [
            origin.strip() for origin in self.cors_origins.split(",") if origin.strip()
        ]


settings = Settings()
