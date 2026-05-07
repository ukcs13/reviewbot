import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import Issue, Review, Severity
from app.schemas.review import AggregatedReview


async def create_review(
    db: AsyncSession, 
    result: AggregatedReview, 
    project_name: str,
    source_type: str,
    source_identifier: str,
    review_time_ms: int,
    user_github_login: Optional[str] = None,
    agent_results: Optional[Dict[str, Any]] = None
) -> Review:
    """
    Persist a complete review and its issues to the database.
    """
    db_review = Review(
        id=uuid.uuid4(),
        project_name=project_name,
        source_type=source_type,
        source_identifier=source_identifier,
        score=result.score,
        review_decision=result.decision,
        summary=result.summary,
        high_count=result.high,
        medium_count=result.medium,
        low_count=result.low,
        info_count=result.info,
        file_count=len(set(i.file_path for i in result.issues if i.file_path)),
        review_time_ms=review_time_ms,
        user_github_login=user_github_login,
        agent_results=agent_results or {}
    )
    
    db.add(db_review)
    await db.flush() # Get the review ID for foreign keys
    
    for issue_data in result.issues:
        db_issue = Issue(
            id=uuid.uuid4(),
            review_id=db_review.id,
            severity=issue_data.severity,
            category=issue_data.category,
            title=issue_data.title,
            message=issue_data.message,
            fix_suggestion=issue_data.fix_suggestion,
            file_path=issue_data.file_path
        )
        db.add(db_issue)
    
    await db.commit()
    await db.refresh(db_review)
    
    # Reload with issues
    stmt = select(Review).where(Review.id == db_review.id).options(selectinload(Review.issues))
    res = await db.execute(stmt)
    return res.scalar_one()

async def get_review_by_id(db: AsyncSession, review_id: uuid.UUID) -> Optional[Review]:
    """Retrieve a single review with its issues."""
    stmt = select(Review).where(Review.id == review_id).options(selectinload(Review.issues))
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def get_reviews(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 20,
    user_login: Optional[str] = None
) -> List[Review]:
    """List reviews with pagination, optionally filtered by user."""
    stmt = select(Review).order_by(desc(Review.created_at)).offset(skip).limit(limit)
    if user_login:
        stmt = stmt.where(Review.user_github_login == user_login)
    
    result = await db.execute(stmt)
    return list(result.scalars().all())

async def get_stats(db: AsyncSession) -> Dict[str, Any]:
    """Calculate application-wide statistics."""
    # Total reviews
    total_reviews = await db.scalar(select(func.count(Review.id))) or 0
    
    # Average score
    avg_score = await db.scalar(select(func.avg(Review.score))) or 0.0
    
    # Total issues found
    total_issues = await db.scalar(select(func.count(Issue.id))) or 0
    
    # Reviews this week
    one_week_ago = datetime.now() - timedelta(days=7)
    reviews_week = await db.scalar(
        select(func.count(Review.id)).where(Review.created_at >= one_week_ago)
    ) or 0
    
    # Issues by severity
    severity_counts = {}
    for sev in Severity:
        count = await db.scalar(
            select(func.count(Issue.id)).where(Issue.severity == sev.value)
        ) or 0
        severity_counts[sev.value] = count
        
    return {
        "total_reviews": total_reviews,
        "average_score": float(avg_score),
        "total_issues_found": total_issues,
        "reviews_this_week": reviews_week,
        "issues_by_severity": severity_counts,
        "top_vulnerable_files": [] # Placeholder for complex query
    }
