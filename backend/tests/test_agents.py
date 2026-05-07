
import pytest

from app.agents.security import SecurityAgent
from app.schemas.review import ProjectContext


@pytest.mark.asyncio
async def test_security_agent_prompt_build():
    agent = SecurityAgent()
    _ = ProjectContext(
        project_name="test",
        files={"main.py": "print('hello')"},
        file_tree=["main.py"],
        languages=["python"]
    )
    prompt = agent.build_prompt("file context", ["Security"])
    assert "Security" in prompt
    assert "OWASP" in prompt

@pytest.mark.asyncio
async def test_security_agent_parse_response():
    agent = SecurityAgent()
    raw_data = {
        "issues": [
            {
                "severity": "high",
                "category": "security",
                "title": "Hardcoded Secret",
                "message": "Secret found in main.py",
                "fix": "Use env var",
                "file": "main.py"
            }
        ]
    }
    result = agent.parse_response(raw_data)
    assert len(result.issues) == 1
    assert result.issues[0].severity.value == "high"
    assert result.issues[0].file_path == "main.py"
