-- Миграция 0001: индексы на внешние ключи и горячие запросы.
-- Применение: psql -U library_user -d library_db -f db/migrations/0001_add_indexes.sql

CREATE INDEX IF NOT EXISTS idx_books_author_id ON books (author_id);
CREATE INDEX IF NOT EXISTS idx_bookings_book_id ON bookings (book_id);
CREATE INDEX IF NOT EXISTS idx_bookings_user_id ON bookings (user_id);
