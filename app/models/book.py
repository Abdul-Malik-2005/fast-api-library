from sqlalchemy import BigInteger, CheckConstraint, UniqueConstraint, ForeignKey, Integer, String, UniqueConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200))
    author_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("authors.id", ondelete="RESTRICT"))
    genre: Mapped[str] = mapped_column(String(50), default="other")
    year: Mapped[int | None] = mapped_column(Integer)
    pages: Mapped[int | None] = mapped_column(Integer)

    author: Mapped["Author"] = relationship(back_populates="books")
    __table_args__ = (
        CheckConstraint("year >= 1450", name="books_year_check"),
        CheckConstraint("pages > 0", name="books_pages_check"),
        UniqueConstraint("title", "author_id", name="books_title_author_id_key"),
    )
