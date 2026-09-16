# Online Library API

Учебный проект курса: backend высоконагруженной онлайн-библиотеки.
Книги, авторы, пользователи, JWT-авторизация и бронирования.
Данные приложения пока живут в памяти; подключение к PostgreSQL настроено и проверяется скриптом (переезд данных на базу — в следующих уроках).

## Технологии

- **Python 3.12** (pyenv + venv)
- **FastAPI** — веб-фреймворк (ASGI)
- **Pydantic v2** — валидация данных и схемы API
- **PostgreSQL** — база данных
- **psycopg** — драйвер подключения к PostgreSQL
- **PyJWT + bcrypt** — JWT-токены и хэширование паролей
- **Ruff** — линтер и форматтер
- **pre-commit** — автоматические проверки перед коммитом

## Установка

1. Клонируй репозиторий и перейди в папку проекта:

```bash
git clone <адрес-репозитория>
cd online_library
```

2. Создай и активируй виртуальное окружение:

```bash
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

3. Установи зависимости:

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

4. Создай `.env` из шаблона и заполни значения:

```bash
copy .env.example .env        # Windows
cp .env.example .env          # Linux / macOS
```

> ⚠️ Файл `.env` содержит секреты и **не коммитится** (добавлен в `.gitignore`).

## База данных

Требуется **PostgreSQL 16 или новее**.

### Установка (Windows)

Скачай инсталлятор с [postgresql.org](https://www.postgresql.org/download/windows/),
в мастере установки запомни пароль суперпользователя `postgres` и оставь порт **5432**.
После установки добавь папку `C:\Program Files\PostgreSQL\<версия>\bin` в переменную `PATH`,
перезапусти терминал и проверь: `psql --version`.

### Создание базы и пользователя проекта

Подключись под суперпользователем (`psql -U postgres`) и выполни:

```sql
CREATE USER library_user WITH PASSWORD 'LibraryDbPass123';
CREATE DATABASE library_db OWNER library_user;
CREATE DATABASE library_test OWNER library_user;   -- для будущих тестов
```

> Замени пароль на свой и обнови его в `.env`.
> Приложение подключается **отдельным пользователем**, а не суперпользователем —
> принцип минимальных привилегий.

### Строка подключения

В `.env`:

```text
DATABASE_URL=postgresql://library_user:LibraryDbPass123@localhost:5432/library_db
```

Анатомия: `postgresql://пользователь:пароль@хост:порт/имя_базы`.

### Проверка соединения

```bash
python -m scripts/check_db
```

Ожидаемый вывод: версия сервера, имя базы и пользователь.

## Запуск

```bash
uvicorn app.main:app --reload
```

- API: http://127.0.0.1:8000/api/v1
- Интерактивная документация (Swagger UI): http://127.0.0.1:8000/docs
- Альтернативная документация (ReDoc): http://127.0.0.1:8000/redoc

## Структура проекта

```text
online_library/
├── app/
│   ├── main.py            # создание приложения, middleware, CORS, lifespan
│   ├── storage.py         # in-memory данные (до переезда на БД)
│   ├── core/
│   │   ├── config.py      # настройки из .env (pydantic-settings)
│   │   └── security.py    # bcrypt-хэши и JWT-токены
│   ├── schemas/           # Pydantic-схемы (book, author, user, booking)
│   └── api/               # роутеры: auth, users, books, authors, bookings, admin
├── scripts/
│   └── check_db.py        # проверка соединения с PostgreSQL
├── tests/                 # тесты (появятся в модуле тестирования)
├── .env.example           # шаблон переменных окружения
├── requirements.txt       # продакшен-зависимости
└── requirements-dev.txt   # dev-инструменты (ruff, pre-commit, httpx)
```

## API (основные эндпоинты)

| Метод | Путь | Описание |
|---|---|---|
| POST | `/api/v1/auth/register` | регистрация пользователя |
| POST | `/api/v1/auth/token` | вход, выдача JWT |
| GET | `/api/v1/users/me` | текущий пользователь |
| GET | `/api/v1/books` | список книг (поиск, пагинация) |
| POST | `/api/v1/books` | создать книгу (нужен вход) |
| DELETE | `/api/v1/books/{id}` | удалить книгу (только админ) |
| GET | `/api/v1/authors` | список авторов |
| POST | `/api/v1/bookings` | забронировать книгу |
| GET | `/api/v1/admin/stats` | статистика (только админ) |

Полный список — в Swagger UI (`/docs`).

### Демо-пользователи

| Логин | Пароль | Роль |
|---|---|---|
| `admin` | `Admin123!` | администратор |
| `reader` | `Reader123!` | обычный читатель |

> Пароли демо-аккаунтов существуют только для учёбы и не используются в продакшене.

## Качество кода

```bash
ruff check .        # проверка линтером
ruff format .       # автоформатирование
```

Хуки `pre-commit` установлены (`pre-commit install`) и прогоняют проверки
при каждом коммите: лишние пробелы, валидность YAML/JSON, ruff.

## Статус курса

Пройдено: окружение и инструменты, FastAPI, Pydantic, авторизация,
продвинутый FastAPI, PostgreSQL и подключение из Python.
Впереди: SQL, ORM, миграции, кэширование, асинхронность.