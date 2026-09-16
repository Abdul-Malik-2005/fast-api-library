"""Бронирования: in-memory реализация (эталон экзамена У9)."""

from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status
from fastapi_projects.library.app.schemas.bookings import (
    BookingCreate,
    BookingResponse,
    BookingStatus,
)

from app.api.deps import AdminUser, CurrentUser, PaginationParams
from app.storage import bookings_db, books_db

router = APIRouter(prefix="/bookings", tags=["Бронирования"])

MAX_ACTIVE_BOOKINGS = 3


def _now() -> datetime:
    return datetime.now(UTC)


def _find_booking(booking_id: int) -> dict | None:
    for booking in bookings_db:
        if booking["id"] == booking_id:
            return booking
    return None


def _is_book_busy(book_id: int) -> bool:
    return any(b["book_id"] == book_id and b["status"] == "active" for b in bookings_db)


def _to_response(booking: dict) -> dict:
    return {
        **booking,
        "is_overdue": booking["status"] == "active" and booking["due_date"] < _now(),
    }


@router.post("", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(booking_in: BookingCreate, current_user: CurrentUser) -> dict:
    """Бронирование с проверкой всех бизнес-правил."""
    if not any(b["id"] == booking_in.book_id for b in books_db):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Книга не найдена")
    if _is_book_busy(booking_in.book_id):
        raise HTTPException(status.HTTP_409_CONFLICT, "Книга уже забронирована")

    active = sum(
        1
        for b in bookings_db
        if b["user_id"] == current_user["id"] and b["status"] == "active"
    )
    if active >= MAX_ACTIVE_BOOKINGS:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Лимит: не более 3 активных бронирований",
        )

    now = _now()
    booking = {
        "id": max((b["id"] for b in bookings_db), default=0) + 1,
        "book_id": booking_in.book_id,
        "user_id": current_user["id"],
        "borrow_date": now,
        "due_date": now + timedelta(days=booking_in.days),
        "return_date": None,
        "status": "active",
    }
    bookings_db.append(booking)
    return _to_response(booking)


@router.get("/my", response_model=list[BookingResponse])
def my_bookings(
    current_user: CurrentUser,
    status_filter: Annotated[BookingStatus | None, Query(alias="status")] = None,
) -> list[dict]:
    """Брони текущего пользователя, новые сверху."""
    result = [b for b in bookings_db if b["user_id"] == current_user["id"]]
    if status_filter is not None:
        result = [b for b in result if b["status"] == status_filter.value]
    result.sort(key=lambda b: b["borrow_date"], reverse=True)
    return [_to_response(b) for b in result]


@router.get("", response_model=list[BookingResponse])
def all_bookings(current_user: AdminUser, pagination: PaginationParams) -> list[dict]:
    """Все брони (только админ) с пагинацией."""
    offset, limit = pagination
    ordered = sorted(bookings_db, key=lambda b: b["borrow_date"], reverse=True)
    return [_to_response(b) for b in ordered[offset : offset + limit]]


@router.post("/{booking_id}/return", response_model=BookingResponse)
def return_booking(booking_id: int, current_user: CurrentUser) -> dict:
    """Возврат книги: владелец или админ."""
    booking = _find_booking(booking_id)
    if booking is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Бронирование не найдено")
    if booking["user_id"] != current_user["id"] and not current_user["is_admin"]:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Можно возвращать только свои бронирования",
        )
    if booking["status"] == "returned":
        raise HTTPException(status.HTTP_409_CONFLICT, "Книга уже возвращена")

    booking["status"] = "returned"
    booking["return_date"] = _now()
    return _to_response(booking)
