import asyncio
import base64
import re

import httpx
import structlog

from app.config import get_settings
from app.schemas.review import ProjectContext

logger = structlog.get_logger()
settings = get_settings()

CODE_EXTENSIONS = {
    ".py", ".ts", ".tsx", ".js", ".jsx", ".java", ".go", ".rb",
    ".php", ".cs", ".cpp", ".c", ".h", ".rs", ".swift", ".kt",
    ".yml", ".yaml", ".toml", ".json", ".env.example", ".sh",
    ".dockerfile", ".md", ".sql", ".html", ".css"
}

SKIP_PATHS = {
    "node_modules", "__pycache__", ".git", "dist", ".next",
    "venv", ".pyc", "build", "coverage", ".pytest_cache",
    "package-lock.json", "yarn.lock", "poetry.lock"
}

PRIORITY_FILES = [
    "main.py", "app.py", "server.py", "index.ts", "index.js",
    "config.py", "settings.py", "config.ts", "next.config.ts",
    "docker-compose.yml", "Dockerfile", ".env.example",
    "pyproject.toml", "package.json", "requirements.txt",
    "auth.py", "security.py", "middleware.py", "models.py",
    "database.py", "db.py", "schema.py", "routes.py", "api.py"
]

async def fetch_project_context(url: str) -> ProjectContext:
    """
    Fetch real file contents from GitHub repository.
    Returns ProjectContext with actual source code for AI analysis.
    """
    # Parse owner/repo from URL
    # Regex updated to be more robust
    match = re.match(r"https://github\.com/([^/]+)/([^/\s\.]+?)(?:\.git)?$", url.strip())
    if not match:
        raise ValueError(f"Invalid GitHub URL: {url}")
    
    owner, repo = match.group(1), match.group(2)
    base = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}

    async with httpx.AsyncClient(timeout=30.0, headers=headers) as client:
        # 1. Get repo metadata
        repo_data = {}
        try:
            r = await client.get(base)
            if r.status_code == 200:
                repo_data = r.json()
            elif r.status_code == 404:
                raise ValueError(f"Repository not found or private: {url}")
        except httpx.TimeoutException:
            logger.warning("github_metadata_timeout", url=url)

        default_branch = repo_data.get("default_branch", "main")
        description = repo_data.get("description", "")
        language = repo_data.get("language", "")
        stars = repo_data.get("stargazers_count", 0)
        open_issues = repo_data.get("open_issues_count", 0)

        # 2. Get full file tree
        all_files = []
        try:
            r = await client.get(f"{base}/git/trees/{default_branch}?recursive=1")
            if r.status_code == 200:
                tree = r.json().get("tree", [])
                all_files = [
                    f["path"] for f in tree
                    if f["type"] == "blob"
                    and not any(skip in f["path"] for skip in SKIP_PATHS)
                    and any(f["path"].endswith(ext) for ext in CODE_EXTENSIONS)
                    and f.get("size", 0) < 100 * 1024  # skip files > 100KB
                ]
        except Exception as e:
            logger.warning("github_tree_error", error=str(e))

        # 3. Select most important files
        selected = _select_files(all_files)
        logger.info("github_files_selected", count=len(selected), repo=f"{owner}/{repo}")

        # 4. Fetch file contents concurrently
        file_contents: dict[str, str] = {}
        async def fetch_file(path: str) -> None:
            try:
                r = await client.get(f"{base}/contents/{path}")
                if r.status_code == 200:
                    data = r.json()
                    if data.get("encoding") == "base64":
                        content = base64.b64decode(data["content"]).decode("utf-8", errors="replace")
                        file_contents[path] = content[:5000]  # first 5000 chars per file
            except Exception as e:
                logger.warning("github_file_fetch_error", path=path, error=str(e))

        await asyncio.gather(*[fetch_file(p) for p in selected[:25]])

        # 5. Get README
        readme = ""
        try:
            r = await client.get(f"{base}/readme")
            if r.status_code == 200:
                data = r.json()
                if data.get("encoding") == "base64":
                    readme = base64.b64decode(data["content"]).decode("utf-8", errors="replace")[:3000]
        except Exception:
            pass

        # 6. Get recent commits for activity context
        recent_commits = []
        try:
            r = await client.get(f"{base}/commits?per_page=5")
            if r.status_code == 200:
                recent_commits = [
                    {"message": c["commit"]["message"][:100], "author": c["commit"]["author"]["name"]}
                    for c in r.json()[:5]
                ]
        except Exception:
            pass

    # Build full context string
    context_parts = [
        f"PROJECT: {owner}/{repo}",
        f"Language: {language}",
        f"Description: {description}",
        f"Stars: {stars} | Open issues: {open_issues}",
        f"Total files found: {len(all_files)}",
        f"Files selected for review: {len(file_contents)}",
        "",
        "FILE TREE (all code files):",
        "\n".join(all_files[:100]),
    ]

    if readme:
        context_parts += ["", "=== README ===", readme]

    if recent_commits:
        context_parts += ["", "=== RECENT COMMITS ==="]
        for c in recent_commits:
            context_parts.append(f"- {c['author']}: {c['message']}")

    context_parts += ["", "=== SOURCE FILES ==="]
    for path, content in file_contents.items():
        context_parts.append(f"\n--- FILE: {path} ---\n{content}")

    full_context = "\n".join(context_parts)
    logger.info("github_context_built",
                repo=f"{owner}/{repo}",
                files_fetched=len(file_contents),
                context_chars=len(full_context))

    return ProjectContext(
        project_name=repo,
        source_type="github_url",
        source_identifier=url,
        file_tree=all_files,
        file_contents=file_contents,
        readme=readme,
        full_context=full_context,
        language=language,
        description=description,
        file_count=len(file_contents),
    )


def _select_files(all_files: list[str]) -> list[str]:
    """Prioritize security-critical and entry-point files."""
    priority, rest = [], []
    for f in all_files:
        filename = f.split("/")[-1].lower()
        if filename in [p.lower() for p in PRIORITY_FILES]:
            priority.append(f)
        elif any(kw in filename for kw in ["auth", "secret", "key", "token", "password", "security", "config", "route", "api", "model", "schema", "db", "database"]):
            priority.append(f)
        else:
            rest.append(f)
    return priority[:20] + rest[:10]
