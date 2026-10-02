from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from app.api.deps import AdminUser, CurrentUser, DbSession, PaginationParams
from app.models import Author, Book
from app.schemas.book import BookCreate, BookResponse, BookUpdate

router = APIRouter(prefix="/books", tags=["Книги"])

def _notify(message: str) -> None:
    print(f"[background] {message}")

def _book_to_dict(book: Book) -> dict:
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author.name,
        "genre": book.genre,
        "year": book.year,
        "pages": book.pages,
    }

def _get_or_create_author(db: DbSession, name: str) -> Author:
    author = db.scalar(select(Author).where(Author.name == name))
    if author is None:
        author = Author(name=name)
        db.add(author)
        db.flush()
    return author

@router.get("", response_model=list[BookResponse])
def get_books(
    db: DbSession,
    pagination: PaginationParams,
    search: str | None = None,
) -> list[dict]:
    stmt = select(Book).options(joinedload(Book.author))

    if search is not None:
        stmt = stmt.where(Book.title.ilike(f"%{search}"))

    offset, limit = pagination
    stmt = stmt.order_by(Book.id).offset(offset).limit(limit)

    books = db.scalar(stmt).all()
    return [_book_to_dict(book) for book in books]


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: DbSession) -> dict:
    book = db.get(Book, book_id, options=[joinedload(Book.author)])
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с id={book_id} не найдена",
        )
    return _book_to_dict(book)


@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(
    book: BookCreate,
    db: DbSession,
    current_user: CurrentUser,
    background_tasks: BackgroundTasks,
) -> dict:
    author = _get_or_create_author(db, book.author)
    new_book = Book(
        title=book.title,
        author=author,
        genre=book.genre.value,
        year=book.year,
        pages=book.pages,
    )
    db.add(new_book)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Такая книга у этого автора уже есть",
        )

    background_tasks.add_task(
        _notify,
        f"Пользователь {current_user['username']} добавил книгу '{book.title}'",
    )
    return _book_to_dict(new_book)


@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, update: BookUpdate, db: DbSession, current_user: CurrentUser) -> dict:
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с id={book_id} не найдена",
        )
    update_data = update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не найдено ни одного поля для обновления",
        )
    if "author" in update_data:
        book.author = _get_or_create_author(db, update_data.pop("author"))
        if "genre" in update_data and update_data["genre"] is not None:
            update_data["genre"] = update_data["genre"].value

        for field, value in update_data.items():
            setattr(book, field, value)
        db.commit()
        return _book_to_dict(book)


@router.delete("/{book_id}")
def delete_book(book_id: int, db: DbSession, current_user: AdminUser) -> dict:
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с id={book_id} не найдена",
        )
    db.delete(book)
    db.commit()

    return {"message": f"Книга с id={book_id} удалена"}

