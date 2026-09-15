"""Роутер для работы с книгами. Данные — в памяти (до У13)."""

from fastapi import APIRouter, BackgroundTasks, HTTPException, status

from app.api.deps import AdminUser, CurrentUser, PaginationParams
from app.schemas.book import BookCreate, BookResponse, BookUpdate, Genre
from app.storage import books_db

router = APIRouter(prefix="/books", tags=["Книги"])


def _notify(message: str) -> None:
    """Имитация фонового действия."""
    print(f"[background] {message}")


def _find_book(book_id: int) -> dict | None:
    for book in books_db:
        if book["id"] == book_id:
            return book
    return None


@router.get("", response_model=list[BookResponse])
def get_books(
    pagination: PaginationParams,
    search: str | None = None,
    genre: Genre | None = None,
) -> list[dict]:
    """Список книг с поиском, фильтром по жанру и пагинацией."""
    result = books_db

    if search is not None:
        search_lower = search.lower()
        result = [
            book
            for book in result
            if search_lower in book["title"].lower()
            or search_lower in book["author"].lower()
        ]
    if genre is not None:
        result = [book for book in result if book["genre"] == genre.value]

    offset, limit = pagination
    return result[offset : offset + limit]


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int) -> dict:
    """Одна книга по её id."""
    book = _find_book(book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с id={book_id} не найдена",
        )
    return book


@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(
    book: BookCreate,
    current_user: CurrentUser,
    background_tasks: BackgroundTasks,
) -> dict:
    """Создание книги + защита от дублей + фоновое уведомление."""
    duplicate = any(
        b["title"].lower() == book.title.lower()
        and b["author"].lower() == book.author.lower()
        for b in books_db
    )
    if duplicate:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Такая книга у этого автора уже есть",
        )

    new_id = max((b["id"] for b in books_db), default=0) + 1
    new_book = {"id": new_id, **book.model_dump()}
    books_db.append(new_book)

    background_tasks.add_task(
        _notify,
        f"Пользователь {current_user['username']} добавил книгу «{book.title}»",
    )
    return new_book


@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, update: BookUpdate, current_user: CurrentUser) -> dict:
    """Обновление только присланных полей (exclude_unset)."""
    book = _find_book(book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с id={book_id} не найдена",
        )

    update_data = update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не передано ни одного поля для обновления",
        )

    book.update(update_data)
    return book


@router.delete("/{book_id}")
def delete_book(book_id: int, current_user: AdminUser) -> dict:
    """Удаление книги: только для администраторов."""
    for index, book in enumerate(books_db):
        if book["id"] == book_id:
            books_db.pop(index)
            return {"message": f"Книга с id={book_id} удалена"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Книга не найдена",
    )