import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.admin import router as admin_router
from app.api.auth import router as auth_router
from app.api.authors import router as authors_router
from app.api.bookings import router as bookings_router
from app.api.books import router as books_router
from app.api.users import router as users_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Жизненный цикл приложения."""
    print("[startup] Online Library API запускается...")
    yield
    print("[shutdown] Закрываем соединения. До встречи!")


app = FastAPI(
    title="Online Library API",
    description="Учебный проект курса: высоконагруженная онлайн-библиотека.",
    version="0.2.0",
    lifespan=lifespan,
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Замер времени обработки каждого запроса."""
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start
    response.headers["X-Process-Time"] = f"{duration:.4f}"
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Роутеры под версионированным префиксом
prefix = settings.api_v1_prefix
app.include_router(auth_router, prefix=prefix)
app.include_router(users_router, prefix=prefix)
app.include_router(books_router, prefix=prefix)
app.include_router(authors_router, prefix=prefix)
app.include_router(bookings_router, prefix=prefix)
app.include_router(admin_router, prefix=prefix)


@app.get("/", tags=["Health"])
def root() -> dict:
    """Проверка жизнеспособности сервиса."""
    return {
        "status": "ok",
        "service": "Online Library API",
        "docs": "/docs",
        "api": prefix,
    }
