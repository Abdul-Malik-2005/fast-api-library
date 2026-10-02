"""Роутер авторов. Данные — в PostgreSQL."""

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.api.deps import DbSession, PaginationParams
from app.models import Author
from app.schemas.author import AuthorResponse

router = APIRouter(prefix="/authors", tags=["Авторы"])


@router.get("", response_model=list[AuthorResponse])
def get_authors(db: DbSession, pagination: PaginationParams) -> list[Author]:
    """Список авторов.

    Здесь можно вернуть сами ORM-объекты: поля схемы совпадают
    с колонками (в У14 добавим моделям режим совместимости).
    """
    offset, limit = pagination
    stmt = select(Author).order_by(Author.id).offset(offset).limit(limit)
    return list(db.scalars(stmt).all())


@router.get("/{author_id}", response_model=AuthorResponse)
def get_author(author_id: int, db: DbSession) -> Author:
    author = db.get(Author, author_id)
    if author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Автор с id={author_id} не найден",
        )
    return author
