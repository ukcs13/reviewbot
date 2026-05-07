from typing import List, Tuple

import structlog

from app.config import get_settings
from app.schemas.review import ProjectContext

logger = structlog.get_logger(__name__)
settings = get_settings()

def select_files_for_review(context: ProjectContext) -> str:
    """
    Priority order for selecting files to send to AI agents.
    Returns a formatted string containing file paths and contents.
    Cap total context at 80,000 chars.
    """
    # Use the unified full_context if available (from GitHub fetcher)
    if context.full_context:
        return context.full_context

    files = context.all_files
    if not files:
        return "No source files available for review."

    # Priority categories (regex-like matches)
    categories = [
        # 1. Security-critical
        ["*auth*", "*secret*", "*key*", "*token*", "*password*", "*cred*"],
        # 2. Config files
        ["config.py", "settings.py", ".env.example", "docker-compose.yml"],
        # 3. Entry points
        ["main.py", "app.py", "index.ts", "server.ts", "index.js", "server.js"],
        # 4. Package files
        ["pyproject.toml", "package.json", "requirements.txt"],
        # 5. API routes
        ["api/", "routes/", "controllers/"],
        # 6. Database
        ["models.py", "schema.py", "migrations/"]
    ]

    selected_files: List[Tuple[str, str]] = []
    seen_paths = set()

    # Apply priority selection
    for patterns in categories:
        for path, content in files.items():
            if path in seen_paths:
                continue
            
            filename = path.lower()
            if any(_match_pattern(pattern, filename) for pattern in patterns):
                selected_files.append((path, content))
                seen_paths.add(path)

    # 7. Add remaining files sorted by size (smallest first)
    remaining = []
    for path, content in files.items():
        if path not in seen_paths:
            remaining.append((path, content))
    
    remaining.sort(key=lambda x: len(x[1]))
    selected_files.extend(remaining)

    # Build context string with 80k char cap
    total_chars = 0
    max_chars = 80000
    context_parts = []
    
    readme = context.readme_text
    if readme:
        readme_summary = f"--- README.md ---\n{readme[:2000]}\n"
        context_parts.append(readme_summary)
        total_chars += len(readme_summary)

    for path, content in selected_files:
        header = f"\n--- File: {path} ---\n"
        if total_chars + len(header) + len(content) > max_chars:
            # If we're over, maybe add just a part of the file if it's important?
            # For now, just stop to be safe.
            break
        
        context_parts.append(header)
        context_parts.append(content)
        total_chars += len(header) + len(content)

    return "".join(context_parts)

def _match_pattern(pattern: str, filename: str) -> bool:
    """Simple glob-like matching."""
    if pattern.startswith("*") and pattern.endswith("*"):
        return pattern[1:-1] in filename
    if pattern.startswith("*"):
        return filename.endswith(pattern[1:])
    if pattern.endswith("*"):
        return filename.startswith(pattern[:-1])
    if pattern.endswith("/"):
        return pattern in filename
    return pattern == filename
