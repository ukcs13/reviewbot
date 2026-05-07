import asyncio
import time
import structlog
from typing import List, Optional, Dict, Any

from app.schemas.review import ProjectContext, AggregatedReview
from app.agents.security import SecurityAgent
from app.agents.quality import QualityAgent
from app.agents.architecture import ArchitectureAgent
from app.core.aggregator import aggregate
from app.core.github_fetcher import fetch_project_context
from app.core.zip_parser import extract_project_context

logger = structlog.get_logger(__name__)

async def run_pipeline(
    source_type: str,
    github_url: Optional[str] = None,
    zip_content: Optional[bytes] = None,
    filename: Optional[str] = None,
    focus_areas: List[str] = None
) -> tuple[AggregatedReview, ProjectContext, int]:
    """
    Orchestrates the full review process:
    1. Fetch/Extract context
    2. Run agents in parallel
    3. Aggregate results
    """
    start_time = time.time()
    focus_areas = focus_areas or []
    
    # 1. Get Context
    if source_type == "github_url":
        if not github_url:
            raise ValueError("GitHub URL required for source_type github_url")
        context = await fetch_project_context(github_url)
    elif source_type == "zip_upload":
        if not zip_content or not filename:
            raise ValueError("ZIP content and filename required for zip_upload")
        context = extract_project_context(zip_content, filename)
    else:
        raise ValueError(f"Invalid source_type: {source_type}")

    # 2. Run Agents in Parallel
    agents = [
        SecurityAgent(),
        QualityAgent(),
        ArchitectureAgent()
    ]
    
    tasks = [agent.run(context, focus_areas) for agent in agents]
    agent_results = await asyncio.gather(*tasks)
    
    # 3. Aggregate
    aggregated = aggregate(agent_results)
    
    review_time_ms = int((time.time() - start_time) * 1000)
    
    logger.info(
        "review_pipeline_completed",
        project=context.project_name,
        score=aggregated.score,
        duration_ms=review_time_ms
    )
    
    return aggregated, context, review_time_ms
