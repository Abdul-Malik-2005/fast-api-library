from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.core.config import settings

_database_url = settings.database_url.replace("postgresql://", "postgresql+psycopg://", 1)
engine = create_engine(_database_url, pool_pre_ping=True, echo=True)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

