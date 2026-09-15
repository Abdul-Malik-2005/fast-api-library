"""Общие зависимости: авторизация, роли, пагинация.

Этот модуль импортируют ВСЕ роутеры, но сам он не импортирует
ни один роутер — так мы избегаем циклических импортов.
"""

from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings
from app.storage import users_db

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.api_v1_prefix}/auth/token"
)


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    """Токен → пользователь. Не распознали — 401."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учётные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.jwt_algorithm]
        )
    except jwt.InvalidTokenError:
        raise credentials_exception

    username = payload.get("sub")
    if username is None:
        raise credentials_exception

    for user in users_db:
        if user["username"] == username:
            return user

    raise credentials_exception


def require_admin(current_user: Annotated[dict, Depends(get_current_user)]) -> dict:
    """Пускаем только администраторов."""
    if not current_user["is_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав",
        )
    return current_user


# Типы-псевдонимы: сигнатуры эндпоинтов читаются как проза
CurrentUser = Annotated[dict, Depends(get_current_user)]
AdminUser = Annotated[dict, Depends(require_admin)]


class Pagination:
    """Зависимость-класс: параметры страницы из query."""

    def __init__(
        self,
        page: int = Query(default=1, ge=1, description="Номер страницы"),
        per_page: int = Query(default=10, ge=1, le=100, description="Размер страницы"),
    ) -> None:
        self.page = page
        self.per_page = per_page

    def __call__(self) -> tuple[int, int]:
        """Возвращает (смещение, лимит) для среза данных."""
        offset = (self.page - 1) * self.per_page
        return offset, self.per_page


PaginationParams = Annotated[tuple[int, int], Depends(Pagination())]