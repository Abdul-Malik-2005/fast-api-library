"""Pydantic-схемы для книг."""

from datetime import UTC, datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator, model_validator


class Genre(str, Enum):
    FICTION = "fiction"
    PROGRAMMING = "programming"
    SCIENCE = "science"
    BIOGRAPHY = "biography"
    OTHER = "other"


class BookBase(BaseModel):
    """Общие поля книги."""

    title: str = Field(min_length=1, max_length=200, examples=["Чистый код"])
    author: str = Field(min_length=3, max_length=100, examples=["Роберт Мартин"])
    genre: Genre = Genre.OTHER
    year: int | None = Field(default=None, ge=1450, examples=[2008])
    pages: int | None = Field(default=None, ge=1, le=10_000)

    @field_validator("title", "author")
    @classmethod
    def strip_and_check(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("поле не может состоять только из пробелов")
        return value

    @model_validator(mode="after")
    def year_not_in_future(self) -> BookBase:
        if self.year is not None and self.year > datetime.now(UTC).year:
            raise ValueError("год издания не может быть в будущем")
        return self


class BookCreate(BookBase):
    """Данные для СОЗДАНИЯ книги. Поля id здесь нет намеренно."""


class BookUpdate(BaseModel):
    """Данные для ОБНОВЛЕНИЯ: все поля необязательные."""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    author: str | None = Field(default=None, min_length=3, max_length=100)
    genre: Genre | None = None
    year: int | None = Field(default=None, ge=1450)
    pages: int | None = Field(default=None, ge=1, le=10_000)


class BookResponse(BookBase):
    """То, что возвращаем клиенту: книга с серверным id."""

    id: int
