from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

import structlog
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.api.health import router as health_router
from app.api.review import router as review_router
from app.api.reviews import router as reviews_router
from app.api.stats import router as stats_router
from app.config import get_settings
from app.db.session import close_db, init_db
from app.exceptions.handlers import register_exception_handlers
from app.middleware.logging import RequestLoggingMiddleware
from app.middleware.rate_limit import setup_rate_limiting

# Configure structured logging
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer() if get_settings().is_production else structlog.dev.ConsoleRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=True,
)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup
    await init_db()
    # redis initialization could go here
    yield
    # Shutdown
    await close_db()

def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="AI Project Reviewer",
        version="1.0.0",
        docs_url="/docs" if not settings.is_production else None,
        redoc_url=None,
        lifespan=lifespan,
    )

    # MIDDLEWARE ORDER IS CRITICAL — add in this EXACT order:
    
    # 1. CORSMiddleware FIRST — before everything else
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            settings.FRONTEND_URL,
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://frontend:3000",
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID"],
    )
    
    # 2. GZip
    app.add_middleware(GZipMiddleware)
    
    # 3. Request logging (custom structlog middleware)
    app.add_middleware(RequestLoggingMiddleware)

    # Setup Rate Limiting
    setup_rate_limiting(app)

    # Register routers
    api_router = APIRouter()
    api_router.include_router(review_router, prefix="/review", tags=["review"])
    api_router.include_router(reviews_router, prefix="/reviews", tags=["reviews"])
    api_router.include_router(stats_router, prefix="/stats", tags=["stats"])
    
    app.include_router(health_router, tags=["health"])
    app.include_router(api_router, prefix="/api")

    # Register exception handlers
    register_exception_handlers(app)

    @app.get("/")
    async def root() -> dict[str, str]:
        return {
            "message": "AI Project Reviewer API",
            "docs": "/docs",
            "health": "/health"
        }

    return app

app = create_app()
