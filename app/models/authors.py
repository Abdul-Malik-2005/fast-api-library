from sqlalchemy import BigInteger, CheckConstraint, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), unique=True)
    country: Mapped[str | None] = mapped_column(String(100))
    birth_year: Mapped[int | None] = mapped_column(Integer)
    books: Mapped[list["Book"]] = relationship(back_populates="author")
    __table_args__ = (CheckConstraint("birth_year >= 1800", name="authors_birth_year_check"),)
