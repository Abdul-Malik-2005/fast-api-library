import psycopg

from app.core.config import settings


def main() -> None:
    with psycopg.connect(settings.database_url) as conn, conn.cursor() as cur:
        cur.execute("SELECT version(), current_database(), current_user")
        version, database, user = cur.fetchone()

        print("Соединение установлено!")
        print(f"Версия: {version}")
        print(f"База: {database}")
        print(f"Пользователь: {user}")


if __name__ == "__main__":
    main()
