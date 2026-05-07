import structlog
from app.schemas.issue import AgentResult, IssueBase
from app.schemas.review import AggregatedReview
from app.db.models import ReviewDecision, Severity

logger = structlog.get_logger(__name__)

def aggregate(results: list[AgentResult]) -> AggregatedReview:
    all_issues = [i for r in results if not r.error for i in r.issues]

    # Check for AI-specific errors (like quota exceeded)
    quota_errors = [r.error for r in results if r.error and "quota" in r.error.lower()]
    if quota_errors:
        return AggregatedReview(
            issues=[IssueBase(
                severity=Severity.high,
                category="system",
                title="AI Analysis Unavailable",
                message="The review pipeline was unable to process your request because the AI service quota has been reached. "
                        "Please try again in a few minutes.",
                fix_suggestion="Wait for the rate limit to reset or check your API configuration.",
                file_path=None,
            )],
            score=0,
            decision=ReviewDecision.critical,
            high=1, medium=0, low=0, info=0,
            summary="Review failed: AI service quota exceeded."
        )

    # If ALL agents failed or returned empty — likely context was not fetched properly
    total_agent_errors = sum(1 for r in results if r.error or len(r.issues) == 0)
    if total_agent_errors == len(results):
        # All agents returned empty — likely context was not fetched properly
        return AggregatedReview(
            issues=[IssueBase(
                severity=Severity.high,
                category="analysis",
                title="Analysis incomplete — no file content fetched",
                message="The review pipeline could not fetch source files from this repository. "
                        "The repository may be private, empty, or the GitHub API rate limit was hit. "
                        "Try again with a different public repository or upload a ZIP file.",
                fix_suggestion="Use a public GitHub URL or upload the project as a ZIP file.",
                file_path=None,
            )],
            score=0,
            decision=ReviewDecision.critical,
            high=1, medium=0, low=0, info=0,
            summary="Review failed: No source files were available for analysis."
        )

    severity_rank = {"high": 4, "medium": 3, "low": 2, "info": 1}
    seen: dict[str, IssueBase] = {}
    for issue in all_issues:
        file_path = issue.file_path or "global"
        key = f"{file_path}:{issue.title[:40].lower()}"
        if key not in seen or severity_rank[issue.severity.value] > severity_rank[seen[key].severity.value]:
            seen[key] = issue

    deduped = sorted(seen.values(),
        key=lambda i: (-severity_rank[i.severity.value], i.category, i.title))

    high   = sum(1 for i in deduped if i.severity == Severity.high)
    medium = sum(1 for i in deduped if i.severity == Severity.medium)
    low    = sum(1 for i in deduped if i.severity == Severity.low)
    info   = sum(1 for i in deduped if i.severity == Severity.info)

    # Realistic scoring — 100 is nearly impossible for real projects
    score = max(0, min(100,
        100 - (high * 20) - (medium * 8) - (low * 3) - (info * 1)
    ))

    # Floor scores based on issue counts — no real project with 5+ issues scores above 85
    if high >= 1: score = min(score, 79)
    if high >= 3: score = min(score, 59)
    if high >= 5: score = min(score, 39)

    if score >= 85:   
        decision = ReviewDecision.excellent
        summary = "This project demonstrates excellent code quality and architecture with minimal issues."
    elif score >= 70: 
        decision = ReviewDecision.good
        summary = "Overall solid implementation with some room for improvement in specific areas."
    elif score >= 50: 
        decision = ReviewDecision.needs_work
        summary = "Significant issues found. Recommendations should be addressed before production."
    else:             
        decision = ReviewDecision.critical
        summary = "Critical vulnerabilities or architectural flaws detected. Immediate action required."

    return AggregatedReview(
        issues=deduped, score=score, decision=decision,
        high=high, medium=medium, low=low, info=info,
        summary=summary
    )
