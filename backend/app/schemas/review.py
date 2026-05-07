import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.db.models import ReviewDecision, SourceType
from app.schemas.issue import IssueBase, IssueItem


class ReviewRequest(BaseModel):
    """Schema for a review request."""
    source_type: SourceType
    github_url: Optional[str] = None
    focus_areas: List[str] = Field(default_factory=list)
    # Note: ZIP file handled via UploadFile in FastAPI

class ReviewBase(BaseModel):
    """Base schema for a review."""
    project_name: str
    source_type: SourceType
    source_identifier: str
    score: int = Field(..., ge=0, le=100)
    review_decision: ReviewDecision
    summary: str
    high_count: int = 0
    medium_count: int = 0
    low_count: int = 0
    info_count: int = 0
    file_count: int = 0
    focus_areas: List[str] = Field(default_factory=list)
    review_time_ms: int

class ReviewCreate(ReviewBase):
    """Schema for creating a new review."""
    user_github_login: Optional[str] = None
    agent_results: Dict[str, Any] = Field(default_factory=dict)
    issues: List[IssueBase] = Field(default_factory=list)

class ReviewResponse(ReviewBase):
    """Schema for a review response."""
    id: uuid.UUID
    user_github_login: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ReviewDetail(ReviewResponse):
    """Detailed review response including issues."""
    issues: List[IssueItem]
    agent_results: Dict[str, Any]

class ProjectContext(BaseModel):
    """Context extracted from a project for AI review."""
    project_name: str
    files: Dict[str, str] = {}
    file_tree: List[str] = []
    readme_content: Optional[str] = None
    languages: List[str] = []
    
    # Fields from GitHub fetcher
    source_type: Optional[str] = None
    source_identifier: Optional[str] = None
    file_contents: Optional[Dict[str, str]] = None
    readme: Optional[str] = None
    full_context: Optional[str] = None
    language: Optional[str] = None
    description: Optional[str] = None
    file_count: int = 0

    @property
    def all_files(self) -> Dict[str, str]:
        """Unified access to files regardless of source."""
        return self.files or self.file_contents or {}

    @property
    def readme_text(self) -> Optional[str]:
        """Unified access to readme."""
        return self.readme_content or self.readme

class AggregatedReview(BaseModel):
    """Result of aggregating agent outputs."""
    issues: List[IssueBase]
    score: int
    decision: ReviewDecision
    high: int
    medium: int
    low: int
    info: int
    summary: str
