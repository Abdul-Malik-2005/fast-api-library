import time
import psycopg

from app.core.config import settings

LIMIT = 50

def native() -> None:
    with psycopg.connect(settings.database_url) as conn, conn.cursor()as cur:
        start = time.perf_counter()
        cur.execute("SELECT id, title, author_id FROM books LIMIT %s", (LIMIT,))
        books = cur.fetchall()
        for _book_id, _title, author_id in books:
            cur.execute("SELECT name FROM authors WHERE id = %s", (author_id,))
            elapsed = time.perf_counter() - start
            print(f'Наивный (1 + N): {elapsed * 1000:7.2f} мс ({1 + len(books)} запросов)')

def optimized() -> None:
    with psycopg.connect(settings.database_url) as conn, conn.cursor() as cur:
        start = time.perf_counter()
        cur.execute(
            """
            SELECT b.title, a.name
            FROM books b
            JOIN authors a ON a.id = b.author_id
            LIMIT %s
            """,
            (LIMIT,),
        )
        cur.fetchall()
        elapsed = time.perf_counter() - start
        print(f"JOIN (1 запрос): {elapsed * 1000:7.2f} мс (1 запрос)")


if __name__ == '__main__':
    native()
    optimized()

        