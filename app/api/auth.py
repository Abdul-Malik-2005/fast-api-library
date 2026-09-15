"""Аутентификация: регистрация и вход.

Охранники живут в deps.py; /me переехал в users.py (У7).
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import create_access_token, hash_password, verify_password
from app.schemas.user import Token, UserCreate, UserResponse
from app.storage import users_db

router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate) -> dict:
    """Регистрация. Пароль сразу превращается в хэш."""
    if any(u["username"] == user_in.username for u in users_db):
        raise HTTPException(status.HTTP_409_CONFLICT, "Имя пользователя занято")
    if any(u["email"] == user_in.email for u in users_db):
        raise HTTPException(status.HTTP_409_CONFLICT, "Email уже используется")

    new_user = {
        "id": max((u["id"] for u in users_db), default=0) + 1,
        "username": user_in.username,
        "email": user_in.email,
        "hashed_password": hash_password(user_in.password),
        "is_admin": False,
    }
    users_db.append(new_user)
    return new_user


@router.post("/token", response_model=Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    """Логин: обмениваем логин+пароль на JWT (форма, не JSON)."""
    user = next(
        (u for u in users_db if u["username"] == form_data.username), None
    )
    if user is None or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=create_access_token(subject=user["username"]))