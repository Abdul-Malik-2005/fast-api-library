-- Схема базы данных онлайн-библиотеки.
-- Применение:  psql -U library_user -d library_db -f db/schema.sql
-- (Linux: добавить -h localhost)

-- Авторы
CREATE TABLE IF NOT EXISTS authors (
    id          BIGSERIAL PRIMARY KEY,
    name        VARCHAR(150) NOT NULL UNIQUE,
    country     VARCHAR(100),
    birth_year  INTEGER CHECK (birth_year >= 1800)
);

-- Книги
CREATE TABLE IF NOT EXISTS books (
    id         BIGSERIAL PRIMARY KEY,
    title      VARCHAR(200) NOT NULL,
    author_id  BIGINT NOT NULL REFERENCES authors(id) ON DELETE RESTRICT,
    genre      VARCHAR(50) NOT NULL DEFAULT 'other',
    year       INTEGER CHECK (year >= 1450),
    pages      INTEGER CHECK (pages > 0),
    -- одна и та же книга одного автора не может существовать дважды
    UNIQUE (title, author_id)
);

-- Пользователи
CREATE TABLE IF NOT EXISTS users (
    id               BIGSERIAL PRIMARY KEY,
    username         VARCHAR(32) NOT NULL UNIQUE,
    email            VARCHAR(254) NOT NULL UNIQUE,
    hashed_password  TEXT NOT NULL,
    is_admin         BOOLEAN NOT NULL DEFAULT FALSE,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Бронирования (помнишь первый экзамен? Теперь они вечные)
CREATE TABLE IF NOT EXISTS bookings (
    id           BIGSERIAL PRIMARY KEY,
    book_id      BIGINT NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    user_id      BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    borrow_date  TIMESTAMPTZ NOT NULL DEFAULT now(),
    due_date     TIMESTAMPTZ NOT NULL,
    return_date  TIMESTAMPTZ,
    status       VARCHAR(10) NOT NULL DEFAULT 'active'
                 CHECK (status IN ('active', 'returned'))
);

