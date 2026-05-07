import asyncio
import json
from abc import ABC, abstractmethod
from json import JSONDecodeError
from typing import Any, ClassVar, List, Optional

import structlog
from openai import AsyncOpenAI
from pydantic import ValidationError

from app.config import get_settings
from app.core.file_selector import select_files_for_review
from app.schemas.issue import AgentResult, IssueBase
from app.schemas.review import ProjectContext

logger = structlog.get_logger(__name__)
settings = get_settings()

class BaseAgent(ABC):
    """
    Base class for AI review agents.
    Handles communication with OpenAI and common parsing logic.
    """
    name: ClassVar[str]
    model_name: Optional[str] = None

    def __init__(self) -> None:
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = self.model_name or settings.OPENAI_MODEL

    async def run(self, context: ProjectContext, focus: List[str]) -> AgentResult:
        """Execute the agent's review logic."""
        file_context = select_files_for_review(context)
        prompt = self.build_prompt(file_context, focus)
        
        try:
            raw = await asyncio.wait_for(
                self._call_openai(prompt),
                timeout=settings.REVIEW_TIMEOUT_SECONDS
            )
            return self._parse_with_retry(raw, prompt)
        except asyncio.TimeoutError:
            logger.warning("agent_timeout", agent=self.name)
            return AgentResult(agent=self.name, issues=[], error="timeout")
        except Exception as e:
            logger.error("agent_error", agent=self.name, error=str(e))
            return AgentResult(agent=self.name, issues=[], error=str(e))

    async def _call_openai(self, prompt: str) -> str:
        """Call the OpenAI API."""
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a senior software engineer performing a code review. You must respond in valid JSON format."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.1,
        )
        return response.choices[0].message.content or "{}"

    def _parse_with_retry(self, raw: str, prompt: str) -> AgentResult:
        """Parse JSON response with basic retry logic."""
        cleaned = raw.strip().removeprefix("```json").removesuffix("```").strip()
        try:
            data = json.loads(cleaned)
            return self.parse_response(data)
        except (ValidationError, JSONDecodeError, KeyError) as e:
            logger.warning("agent_parse_error", agent=self.name, error=str(e))
            # In a real scenario, we might want to retry with a stricter prompt here
            return AgentResult(agent=self.name, issues=[], error="parse_failed")

    @abstractmethod
    def build_prompt(self, file_context: str, focus: List[str]) -> str:
        """Build the system/user prompt for the agent."""
        pass

    def parse_response(self, data: dict[str, Any]) -> AgentResult:
        """Parse the JSON dictionary into an AgentResult."""
        issues = []
        for issue_data in data.get("issues", []):
            try:
                # Map 'file' from AI response to 'file_path' in our schema
                if "file" in issue_data:
                    issue_data["file_path"] = issue_data.pop("file")
                # Map 'fix' from AI response to 'fix_suggestion' in our schema
                if "fix" in issue_data:
                    issue_data["fix_suggestion"] = issue_data.pop("fix")
                issues.append(IssueBase(**issue_data))
            except ValidationError as e:
                logger.warning("issue_validation_error", error=str(e), data=issue_data)
        
        return AgentResult(agent=self.name, issues=issues)
