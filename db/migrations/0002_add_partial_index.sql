-- Применение:
--   psql -U library_user -d library_db -h localhost -f db/migrations/0002_add_partial_index.sql


CREATE INDEX if NOT EXISTS idx_booking_active
    on bookings (book_id)
    where status = 'active';