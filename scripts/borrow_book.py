import psycopg

from app.core.config import settings

BOOK_ID = 2
USERNAME = 'reader'

def main() -> None:
    with psycopg.connect(settings.database_url) as conn:

        with conn.transaction():
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id FROM books WHERE id = %s FOR UPDATE",
                    (BOOK_ID,),
                )
                if cur.fetchone() is None:
                    raise LookupError(f"Книга с id={BOOK_ID} не найдена")

                cur.execute(
                    """
                    SELECT 1 FROM bookings
                    WHERE book_id = %s AND status = 'active'
                    """,
                    (BOOK_ID,),
                )
                if cur.fetchone() is not None:
                    raise RuntimeError("Книга уже заброинрвана")

                cur.execute(
                    """
                    INSERT INTO bookings (book_id, user_id, due_date)
                    SELECT %s, id, now() + INTERVAL '14 days'
                    FROM users
                    WHERE username = %s
                    RETURNING id
                    """,
                    (BOOK_ID, USERNAME),

                )
                booking_id = cur.fetchone()[0]

    print(f"Бронь №{booking_id} создана")


if __name__ == '__main__':
    try:
        main()
    except RuntimeError as exc:
        print(f"Отказ: {exc}")
    except LookupError as exc:
        print(f"Отказ: {exc}")