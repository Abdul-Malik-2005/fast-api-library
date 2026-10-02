"""Админские эндпоинты: весь роутер защищён целиком."""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from app.api.deps import require_admin, DbSession
from app.storage import users_db
from app.models import Author, Book

router = APIRouter(
    prefix="/admin",
    tags=["Админ"],
    dependencies=[Depends(require_admin)],
)


@router.get("/stats")
def stats(db: DbSession) -> dict:
    """Сводная статистика библиотеки."""
    return {
        "books": db.scalar(select(func.count()).select_from(Book)),
        "authors": db.scalar(select(func.count).select_from(Author)),
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
