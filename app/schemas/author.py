"""Pydantic-схемы для авторов."""

from pydantic import BaseModel, Field, field_validator


class AuthorCreate(BaseModel):
    name: str = Field(min_length=3, max_length=150)
    country: str = Field(min_length=2)
    birth_year: int = Field(ge=1800)

    @field_validator("name")
    @classmethod
    def strip_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("имя не может состоять только из пробелов")
        return value


class AuthorResponse(AuthorCreate):
    id: int