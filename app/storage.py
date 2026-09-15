"""In-memory «база данных» учебного проекта.

Начиная с У13 этот модуль будет заменён реальным подключением к PostgreSQL.
"""

from app.core.security import hash_password

# --- Пользователи ----------------------------------------------
users_db: list[dict] = [
    {
        "id": 1,
        "username": "admin",
        "email": "admin@library.local",
        "hashed_password": hash_password("Admin123!"),  # только для учёбы!
        "is_admin": True,
    },
    {
        "id": 2,
        "username": "reader",
        "email": "reader@library.local",
        "hashed_password": hash_password("Reader123!"),
        "is_admin": False,
    },
]

# --- Книги ------------------------------------------------------
books_db: list[dict] = [
    {"id": 1, "title": "Чистый код", "author": "Роберт Мартин", "genre": "programming", "year": 2008, "pages": 464},
    {"id": 2, "title": "Совершенный код", "author": "Стив Макконнелл", "genre": "programming", "year": 2004, "pages": 914},
    {"id": 3, "title": "Мастер и Маргарита", "author": "Михаил Булгаков", "genre": "fiction", "year": 1967, "pages": 480},
]

# --- Авторы -----------------------------------------------------
authors_db: list[dict] = [
    {"id": 1, "name": "Роберт Мартин", "country": "США", "birth_year": 1952},
    {"id": 2, "name": "Стив Макконнелл", "country": "США", "birth_year": 1962},
    {"id": 3, "name": "Михаил Булгаков", "country": "Россия", "birth_year": 1891},
]

# --- Бронирования (экзамен У9) -----------------------------------
bookings_db: list[dict] = []