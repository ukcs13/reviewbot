from fastapi import FastAPI, Request, Response
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

# Initialize limiter
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

def setup_rate_limiting(app: FastAPI) -> None:
    """Setup rate limiting for the FastAPI application."""
    app.state.limiter = limiter
    # Register handler
    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request: Request, exc: Exception) -> Response:
        return await _rate_limit_exceeded_handler(request, exc) # type: ignore
