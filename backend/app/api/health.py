import redis.asyncio as redis
from typing import Any, cast
from fastapi import APIRouter, Response, status
from sqlalchemy import select

from app.config import get_settings
from app.db.session import engine

router = APIRouter()
settings = get_settings()

@router.get("/health")
async def health_check() -> dict[str, str]:
    """Simple health check for load balancers."""
    return {"status": "ok", "version": "1.0.0"}

@router.get("/ready")
async def readiness_check(response: Response) -> dict[str, str]:
    """Detailed readiness check verifying DB and Redis connections."""
    db_status = "connected"
    redis_status = "connected"
    is_ready = True

    # Check Database
    try:
        async with engine.connect() as conn:
            await conn.execute(select(1))
    except Exception:
        db_status = "error"
        is_ready = False

    # Check Redis
    try:
        # Using Any and type ignore to bypass library-specific typing issues across different environments
        r: Any = redis.from_url(settings.REDIS_URL)  # type: ignore
        await r.ping()
        await r.close()
    except Exception:
        redis_status = "error"
        is_ready = False

    if not is_ready:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {
            "status": "not_ready",
            "database": db_status,
            "redis": redis_status
        }

    return {
        "status": "ready",
        "database": db_status,
        "redis": redis_status
    }
