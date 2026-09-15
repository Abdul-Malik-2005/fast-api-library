"""Админские эндпоинты: весь роутер защищён целиком."""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import require_admin
from app.storage import authors_db, books_db, users_db

router = APIRouter(
    prefix="/admin",
    tags=["Админ"],
    dependencies=[Depends(require_admin)],
)


@router.get("/stats")
def stats() -> dict:
    """Сводная статистика библиотеки."""
    return {
        "books": len(books_db),
        "authors": len(authors_db),
        "users": len(users_db),
    }


def get_fake_session():
    """Паттерн управления ресурсом (репетиция сессий БД из У13)."""
    session = {"id": str(uuid.uuid4())[:8], "queries": 0}
    print(f"[db] сессия {session['id']} ОТКРЫТА")
    try:
        yield session
    finally:
        print(f"[db] сессия {session['id']} ЗАКРЫТА")


FakeSession = Annotated[dict, Depends(get_fake_session)]


@router.get("/db-info")
def db_info(session: FakeSession) -> dict:
    """Демонстрация зависимости с yield."""
    session["queries"] += 1
    return {"session_id": session["id"], "queries": session["queries"]}