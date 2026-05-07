# AI Project Reviewer

An instant AI-powered code review tool. Upload a GitHub URL or a ZIP file and get a production-grade code audit in seconds.

## Features

- **GitHub Integration**: Review any public repository by URL.
- **ZIP Upload**: Audit local projects up to 50MB.
- **Multi-Agent Analysis**:
  - **Security Agent**: Checks for OWASP vulnerabilities and hardcoded secrets.
  - **Quality Agent**: Audits code maintainability, complexity, and best practices.
  - **Architecture Agent**: Reviews system design, Docker practices, and API structure.
- **Actionable Fixes**: Every issue includes a specific recommendation to improve your code.
- **Production-Ready**: Built with FastAPI, Next.js 14, PostgreSQL, and Redis.

## Tech Stack

- **Backend**: Python 3.12, FastAPI, SQLAlchemy 2.0, PostgreSQL 16.
- **AI**: Google Gemini 2.0 Flash.
- **Cache**: Redis 7.
- **Frontend**: Next.js 14 (App Router), TypeScript, Tailwind CSS.
- **Auth**: NextAuth.js v5 with GitHub OAuth.
- **Deployment**: Docker, Docker Compose.

## Getting Started

### Prerequisites

- Docker and Docker Compose
- GitHub OAuth Application credentials
- Gemini API Key

### Setup

1. Clone the repository.
2. Create a `.env` file in the root directory using the following template:

```env
NEXTAUTH_SECRET=your_generated_secret
GITHUB_CLIENT_ID=your_github_id
GITHUB_CLIENT_SECRET=your_github_secret
GEMINI_API_KEY=your_gemini_key
```

3. Start the application:

```bash
docker compose up --build
```

4. Access the app at `http://localhost:3000`.

## Development

### Backend

```bash
cd backend
pip install uv
uv pip install --system .
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## License

MIT
