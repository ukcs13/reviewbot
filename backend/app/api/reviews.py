import uuid
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import repositories
from app.db.session import get_db
from app.dependencies import get_optional_user
from app.schemas.review import ReviewDetail, ReviewResponse

router = APIRouter()

@router.get("", response_model=List[ReviewResponse])
async def list_reviews(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: Optional[dict[str, Any]] = Depends(get_optional_user)
) -> Any:
    """
    List reviews with pagination. 
    If logged in, shows user's reviews. Otherwise shows public reviews.
    """
    user_login = current_user.get("login") if current_user else None
    reviews = await repositories.get_reviews(db, skip=skip, limit=limit, user_login=user_login)
    return reviews

@router.get("/{review_id}", response_model=ReviewDetail)
async def get_review(
    review_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get detailed results for a specific review."""
    review = await repositories.get_review_by_id(db, review_id)
    if not review:
        raise HTTPException(404, "Review not found")
    return review
