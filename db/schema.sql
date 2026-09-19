CREATE TABLE IF NOT EXISTS authors (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE,
    country varchar(100),
    birth_year INTEGER CHECK (birth_year >=1000)
);

CREATE TABLE if not EXISTS books (
    id bigserial PRIMARY KEY,
    title varchar(200) not null unique,
    author_id bigint not null REFERENCES authors(id) on DELETE RESTRICT,
    genre varchar(50) not null DEFAULT 'other',
    year integer CHECK (year >= 1450),
    pages integer CHECK (pages > 0),
    UNIQUE (title, author_id)
);


CREATE TABLE if not EXISTS users (
    id bigserial PRIMARY KEY,
    username varchar(32) not null UNIQUE,
    email varchar(254) not null UNIQUE,
    hashed_password text not null,
    is_admin boolean not null default false,
    created_at timestamptz not null DEFAULT now()
);

CREATE table if not EXISTS bookings (
    id bigserial primary key,
    book_id bigint not null REFERENCES books(id) on delete CASCADE,
    user_id bigint not null REFERENCES users(id) in DELETE CASCADE,
    borrow_date timestamptz not null DEFAULT now(),
    due_date timestamptz not null,
    return_date timestamptz,
    status varchar(10) not null DEFAULT 'active' CHECK (status IN ('active', 'returned'))
);