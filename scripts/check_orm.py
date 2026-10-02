from sqlalchemy import func, select
from app.core.db import SessionLocal
from app.models import Book

def main() -> None:
    with SessionLocal() as session:
        total = session.scalar(select(func.count()).select_from(Book))
        print(f"Всего книг в базе: {total}")
        books = session.scalars(select(Book).order_by(Book.id).limit(5)).all()
        for book in books:
            print(f" #{book.id} {book.title} ({book.genre}, {book.year})")


if __name__ == "__main__":
    main()
