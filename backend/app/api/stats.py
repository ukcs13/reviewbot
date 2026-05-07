from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import repositories
from app.db.session import get_db
from app.schemas.stats import StatsResponse

router = APIRouter()

@router.get("", response_model=StatsResponse)
async def get_application_stats(db: AsyncSession = Depends(get_db)) -> dict[str, Any]:
    """Get aggregate statistics for the dashboard."""
    stats = await repositories.get_stats(db)
    return stats
