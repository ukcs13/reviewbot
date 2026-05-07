import uuid
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.db.models import Severity


class IssueBase(BaseModel):
    """Base schema for an issue."""
    severity: Severity
    category: str = Field(..., max_length=50)
    title: str = Field(..., max_length=255)
    message: str
    fix_suggestion: str
    file_path: Optional[str] = Field(None, max_length=512)

class IssueCreate(IssueBase):
    """Schema for creating a new issue."""
    pass

class IssueItem(IssueBase):
    """Schema for an issue item returned in responses."""
    id: uuid.UUID
    
    model_config = ConfigDict(from_attributes=True)

class AgentResult(BaseModel):
    """Result from a single AI agent."""
    agent: str
    issues: List[IssueBase]
    error: Optional[str] = None
