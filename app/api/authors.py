"""Роутер авторов."""

from fastapi import APIRouter, HTTPException, status

from app.api.deps import PaginationParams
from app.schemas.author import AuthorResponse
from app.storage import authors_db

router = APIRouter(prefix="/authors", tags=["Авторы"])


def _find_author(author_id: int) -> dict | None:
    for author in authors_db:
        if author["id"] == author_id:
            return author
    return None


@router.get("", response_model=list[AuthorResponse])
def get_authors(pagination: PaginationParams) -> list[dict]:
    """Список авторов с пагинацией."""
    offset, limit = pagination
    return authors_db[offset : offset + limit]


@router.get("/{author_id}", response_model=AuthorResponse)
def get_author(author_id: int) -> dict:
    """Один автор по id."""
    author = _find_author(author_id)
    if author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Автор с id={author_id} не найден",
        )
    return author