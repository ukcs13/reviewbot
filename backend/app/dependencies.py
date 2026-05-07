from typing import Any, Optional

import structlog
from fastapi import Depends, HTTPException, Request

from app.config import get_settings

logger = structlog.get_logger(__name__)
settings = get_settings()

async def get_optional_user(request: Request) -> Optional[dict[str, Any]]:
    """
    Optional user dependency. 
    Returns the user profile if a valid GitHub session token is present.
    """
    # In a real app, you'd validate the session token from cookies or Auth header
    # For now, this is a placeholder that would be used with NextAuth
    return None

async def get_required_user(user: Optional[dict[str, Any]] = Depends(get_optional_user)) -> dict[str, Any]:
    """Ensure a user is authenticated."""
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user
