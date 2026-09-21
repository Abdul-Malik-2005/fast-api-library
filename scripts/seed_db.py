"""Наполнение базы начальными данными.

Запуск из корня проекта:  python -m scripts.seed_db
"""

import psycopg

from app.core.config import settings
from app.core.security import hash_password

AUTHORS = [
    {"name": "Роберт Мартин", "country": "США", "birth_year": 1952},
    {"name": "Стив Макконнелл", "country": "США", "birth_year": 1962},
    {"name": "Михаил Булгаков", "country": "Россия", "birth_year": 1891},
]

BOOKS = [
    {
        "title": "Чистый код",
        "author": "Роберт Мартин",
        "genre": "programming",
        "year": 2008,
        "pages": 464,
    },
    {
        "title": "Совершенный код",
        "author": "Стив Макконнелл",
        "genre": "programming",
        "year": 2004,
        "pages": 914,
    },
    {
        "title": "Мастер и Маргарита",
        "author": "Михаил Булгаков",
        "genre": "fiction",
        "year": 1967,
        "pages": 480,
    },
]

USERS = [
    {
        "username": "admin",
        "email": "admin@library.local",
        "password": "Admin123!",
        "is_admin": True,
    },
    {
        "username": "reader",
        "email": "reader@library.local",
        "password": "Reader123!",
        "is_admin": False,
    },
]


def main() -> None:
    with psycopg.connect(settings.database_url) as conn:
        with conn.cursor() as cur:
            # --- Авторы: параметры вида %(имя)s берутся из словаря ---
            for author in AUTHORS:
                cur.execute(
                    """
                    INSERT INTO authors (name, country, birth_year)
                    VALUES (%(name)s, %(country)s, %(birth_year)s)
                    ON CONFLICT (name) DO NOTHING
                    """,
                    author,
                )

            # --- Книги: автора находим подзапросом по имени ---
            for book in BOOKS:
                cur.execute(
                    """
                    INSERT INTO books (title, author_id, genre, year, pages)
                    VALUES (
                        %(title)s,
                        (SELECT id FROM authors WHERE name = %(author)s),
                        %(genre)s,
                        %(year)s,
                        %(pages)s
                    )
                    ON CONFLICT (title, author_id) DO NOTHING
                    """,
                    book,
                )

            # --- Пользователи: хэшируем пароль тем же кодом, что и приложение ---
            for user in USERS:
                cur.execute(
                    """
                    INSERT INTO users (username, email, hashed_password, is_admin)
                    VALUES (%(username)s, %(email)s, %(hash)s, %(is_admin)s)
                    ON CONFLICT (username) DO NOTHING
                    """,
                    {**user, "hash": hash_password(user["password"])},
                )

            # --- Демо-бронь: книга «Чистый код» у читателя, вернуть через 14 дней ---
            cur.execute("""
                INSERT INTO bookings (book_id, user_id, due_date)
                SELECT b.id, u.id, now() + INTERVAL '14 days'
                FROM books b, users u
                WHERE b.title = 'Чистый код'
                  AND u.username = 'reader'
                  AND NOT EXISTS (SELECT 1 FROM bookings)
                """)

        conn.commit()  # фиксируем всё одной транзакцией — помнишь букву A из ACID?

    print("✅ База наполнена данными")


if __name__ == "__main__":
    main()
