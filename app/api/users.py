"""Публичные эндпоинты пользователей."""

from fastapi import APIRouter

from app.api.deps import CurrentUser
from app.schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.get("/me", response_model=UserResponse)
def me(current_user: CurrentUser) -> dict:
    """Информация о текущем пользователе."""
    return current_user
