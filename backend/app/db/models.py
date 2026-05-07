import enum
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all database models."""
    pass


class SourceType(str, enum.Enum):
    """Types of project sources."""
    github_url = "github_url"
    zip_upload = "zip_upload"


class ReviewDecision(str, enum.Enum):
    """Review outcome decisions."""
    excellent = "excellent"
    good = "good"
    needs_work = "needs_work"
    critical = "critical"


class Severity(str, enum.Enum):
    """Issue severity levels."""
    high = "high"
    medium = "medium"
    low = "low"
    info = "info"


class Review(Base):
    """
    Review model storing aggregated results of a project review.
    """
    __tablename__ = "reviews"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_github_login: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    source_type: Mapped[SourceType] = mapped_column(Enum(SourceType), nullable=False)
    source_identifier: Mapped[str] = mapped_column(String(500), nullable=False)
    project_name: Mapped[str] = mapped_column(String(255), nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    review_decision: Mapped[ReviewDecision] = mapped_column(Enum(ReviewDecision), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Issue counts
    high_count: Mapped[int] = mapped_column(Integer, default=0)
    medium_count: Mapped[int] = mapped_column(Integer, default=0)
    low_count: Mapped[int] = mapped_column(Integer, default=0)
    info_count: Mapped[int] = mapped_column(Integer, default=0)
    file_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # Metadata
    focus_areas: Mapped[List[str]] = mapped_column(JSONB, default=list)
    agent_results: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict)
    review_time_ms: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relationships
    issues: Mapped[List["Issue"]] = relationship("Issue", back_populates="review", cascade="all, delete-orphan")


class Issue(Base):
    """
    Individual issue found during a review.
    """
    __tablename__ = "issues"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    review_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("reviews.id", ondelete="CASCADE"), nullable=False)
    severity: Mapped[Severity] = mapped_column(Enum(Severity), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    fix_suggestion: Mapped[str] = mapped_column(Text, nullable=False)
    file_path: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relationships
    review: Mapped["Review"] = relationship("Review", back_populates="issues")
