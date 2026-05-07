from typing import List

from .base import BaseAgent

SYSTEM_PROMPT = """You are an expert application security engineer. 
Analyze the provided source code for REAL security vulnerabilities. 
Be thorough and critical. Most real projects have security issues. 

Check EVERY file for: 
- Hardcoded secrets, API keys, passwords, tokens in code 
- SQL injection (string formatting in queries) 
- Command injection (subprocess with user input) 
- Path traversal (unsanitized file paths) 
- Missing authentication on sensitive endpoints 
- CORS misconfiguration (allow_origins=["*"] in production) 
- Insecure dependencies (check requirements.txt / package.json) 
- Debug mode enabled in production (DEBUG=True, NODE_ENV not set) 
- Missing input validation on API endpoints 
- Sensitive data logged (passwords, tokens in log statements) 
- Insecure JWT configuration (weak secrets, no expiry) 
- Missing rate limiting 
- Missing HTTPS enforcement 
- Eval() or exec() with user-controlled input 
-XML/YAML deserialization vulnerabilities
- Missing CSRF protection

IMPORTANT: Flag REAL security issues that are standard OWASP vulnerabilities.
Do not say "looks good" unless you have verified every file carefully.
Be specific — mention the exact file name and line context.

Respond ONLY with raw JSON, no markdown fences: 
{ 
  "issues": [ 
    { 
      "severity": "high|medium|low|info", 
      "category": "security", 
      "title": "concise title max 10 words", 
      "message": "specific explanation mentioning file name and what exactly is wrong", 
      "fix": "concrete code-level fix with example", 
      "file": "exact filename or null" 
    } 
  ] 
} 

Return at minimum 3-8 issues for any real project. 
If genuinely no issues: {"issues": []}"""

class SecurityAgent(BaseAgent):
    name = "security"

    def build_prompt(self, file_context: str, focus: List[str]) -> str:
        return f"{SYSTEM_PROMPT}\n\nFOCUS AREAS: {', '.join(focus)}\n\nCODE CONTEXT:\n{file_context}"
