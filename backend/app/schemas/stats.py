from typing import Dict, List

from pydantic import BaseModel


class StatsResponse(BaseModel):
    """Schema for application-wide statistics."""
    total_reviews: int
    average_score: float
    total_issues_found: int
    reviews_this_week: int
    issues_by_severity: Dict[str, int]
    top_vulnerable_files: List[Dict[str, str | int]]
