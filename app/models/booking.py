from datetime import datetime

from sqlalchemy import BigInteger, CheckConstraint, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Booking(Base):
    __tablename__ = "bookings"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    book_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("books.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    borrow_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    due_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    return_date: Mapped[str] = mapped_column(String(10), default="active")

    book: Mapped["Book"] = relationship()
    user: Mapped["User"] = relationship()
    __table_args__ = (
        CheckConstraint("status IN ('active', 'returned')", name="bookings_status_check"),
    )
