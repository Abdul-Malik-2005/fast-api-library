"""Схемы бронирований (экзамен У9)."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class BookingStatus(str, Enum):
    ACTIVE = "active"
    RETURNED = "returned"


class BookingCreate(BaseModel):
    book_id: int = Field(ge=1)
    days: int = Field(ge=1, le=30, description="Срок аренды в днях")


class BookingResponse(BaseModel):
    id: int
    book_id: int
    user_id: int
    borrow_date: datetime
    due_date: datetime
    return_date: datetime | None
    status: BookingStatus
    is_overdue: bool