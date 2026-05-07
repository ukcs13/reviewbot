import json
import structlog
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.db import repositories
from app.schemas.review import ReviewResponse
from app.core import review_pipeline
from app.config import get_settings
from app.dependencies import get_optional_user

router = APIRouter()
logger = structlog.get_logger(__name__)
settings = get_settings()

@router.post("", response_model=ReviewResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_review(
    source_type: str = Form(...),          # "github_url" or "zip_upload"
    github_url: str | None = Form(None),
    focus_areas: str = Form("[]"),         # JSON string of selected areas
    file: UploadFile | None = File(None),  # ZIP file for zip_upload mode
    db: AsyncSession = Depends(get_db),
    current_user: Optional[dict] = Depends(get_optional_user),
):
    """
    Accept review request, validate input, run pipeline, return result.
    For ZIP uploads: validate size, extension, and content.
    For GitHub URLs: validate URL format before fetching.
    """
    # 1. Validate input
    content = None
    filename = None
    source_identifier = ""

    if source_type == "github_url":
        if not github_url or not github_url.startswith("https://github.com/"):
            raise HTTPException(422, "Invalid GitHub URL. Must start with https://github.com/")
        source_identifier = github_url
    elif source_type == "zip_upload":
        if not file or not file.filename.endswith(".zip"):
            raise HTTPException(422, "Must upload a .zip file")
        
        content = await file.read()
        if len(content) > settings.max_zip_bytes:
            raise HTTPException(413, f"ZIP exceeds {settings.MAX_ZIP_SIZE_MB}MB limit")
        
        filename = file.filename
        source_identifier = filename
    else:
        raise HTTPException(422, "source_type must be github_url or zip_upload")

    try:
        parsed_focus_areas = json.loads(focus_areas)
    except json.JSONDecodeError:
        raise HTTPException(422, "focus_areas must be a valid JSON list of strings")

    # 2. Run review pipeline (synchronous — wait for result in this version)
    # In a real high-traffic app, we'd use Celery/Arq here.
    try:
        aggregated_result, context, review_time_ms = await review_pipeline.run_pipeline(
            source_type=source_type,
            github_url=github_url,
            zip_content=content,
            filename=filename,
            focus_areas=parsed_focus_areas
        )
    except Exception as e:
        logger.error("pipeline_execution_failed", error=str(e))
        raise HTTPException(500, f"Review pipeline failed: {str(e)}")

    # 3. Persist to DB
    user_login = current_user.get("login") if current_user else None
    
    review = await repositories.create_review(
        db=db,
        result=aggregated_result,
        project_name=context.project_name,
        source_type=source_type,
        source_identifier=source_identifier,
        review_time_ms=review_time_ms,
        user_github_login=user_login,
        agent_results={} # Raw results could be added here if needed
    )
    
    return review
