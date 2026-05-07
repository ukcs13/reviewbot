# AI Project Reviewer 🚀

An instant AI-powered code review tool. Provide a GitHub URL or upload a ZIP file to receive a production-grade code audit in seconds.

## ✨ Features

- **GitHub Integration**: Review any public repository directly via its URL.
- **ZIP Upload**: Audit local projects (up to 50MB) with ease.
- **Multi-Agent Analysis**:
  - **Security Agent**: Identifies OWASP vulnerabilities, hardcoded secrets, and security flaws.
  - **Quality Agent**: Audits code maintainability, complexity, and language-specific best practices.
  - **Architecture Agent**: Reviews system design, Docker configurations, and API structures.
- **Actionable Fixes**: Every identified issue includes concrete recommendations for improvement.
- **Real-time Feedback**: Detailed reports with severity levels and specific file references.

## 🛠 Tech Stack

- **Backend**: Python 3.12, FastAPI, SQLAlchemy 2.0, PostgreSQL 16.
- **AI**: **OpenAI GPT-4o** (with native JSON mode for reliability).
- **Cache**: Redis 7 (for rate limiting and session management).
- **Frontend**: Next.js 14 (App Router), TypeScript, Tailwind CSS, Shadcn UI.
- **Auth**: NextAuth.js v5 with GitHub OAuth integration.
- **Deployment**: Docker & Docker Compose.

## 🚀 Getting Started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed.
- A GitHub OAuth Application ([Create one here](https://github.com/settings/developers)).
- An OpenAI API Key.

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ukcs13/reviewbot.git
   cd reviewbot
   ```

2. **Configure Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   # Frontend / Auth
   NEXTAUTH_SECRET=your_generated_secret
   GITHUB_CLIENT_ID=your_github_id
   GITHUB_CLIENT_SECRET=your_github_secret
   
   # Backend
   OPENAI_API_KEY=your_openai_key
   OPENAI_MODEL=gpt-4o
   ```

3. **Launch with Docker**:
   ```bash
   docker compose up --build
   ```

4. **Access the Application**:
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## 🏗 Development

### Backend (Local)
The backend uses `uv` for lightning-fast dependency management.
```bash
cd backend
# Using uv (recommended)
uv pip install --system .
# Or using pip
pip install -e .
uvicorn app.main:app --reload
```

### Frontend (Local)
```bash
cd frontend
npm install
npm run dev
```

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---
Built by [ukcs13](https://github.com/ukcs13)
