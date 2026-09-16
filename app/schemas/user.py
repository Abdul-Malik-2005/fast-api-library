"""Схемы пользователей и токенов."""

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=32, examples=["reader"])
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    @field_validator("password")
    @classmethod
    def password_strength(cls, value: str) -> str:
        if not any(char.isdigit() for char in value):
            raise ValueError("пароль должен содержать хотя бы одну цифру")
        if not any(char.isalpha() for char in value):
            raise ValueError("пароль должен содержать хотя бы одну букву")
        if not any(char.isupper() for char in value):
            raise ValueError("пароль должен содержать хотя бы одну заглавную букву")
        if not any(char in "!@#$%^&*()_+-=" for char in value):
            raise ValueError("пароль должен содержать хотя бы один спецсимвол")
        return value


class UserResponse(BaseModel):
    """Публичный контракт: НИКАКИХ паролей и хэшей."""

    id: int
    username: str
    email: EmailStr
    is_admin: bool


class Token(BaseModel):
    """Ответ эндпоинта логина (схема OAuth2)."""

    access_token: str
    token_type: str = "bearer"
