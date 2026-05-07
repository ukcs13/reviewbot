from typing import Optional

import structlog
from fastapi import Depends, HTTPException, Request

from app.config import get_settings

logger = structlog.get_logger(__name__)
settings = get_settings()

async def get_optional_user(request: Request) -> Optional[dict]:
    """
    Extract user info from NextAuth session/JWT if available.
    Backend validates the session if needed, or trusts the header if behind a proxy.
    For this implementation, we'll look for an 'X-User-Login' header 
    which would be set by a secure gateway or the frontend if we trust it.
    """
    # In a production app, we would verify the NextAuth JWT here
    # using jose or by calling an auth service.
    user_login = request.headers.get("X-User-Login")
    if user_login:
        return {"login": user_login}
    return None

async def get_required_user(user: Optional[dict] = Depends(get_optional_user)) -> dict:
    """Ensure a user is authenticated."""
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user
