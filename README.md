# AI Interviewer

Stage 1 — Scaffold and Quality Gates. No auth, upload, LangGraph, interview, voice, avatar, dashboard.

## Struktur

```
apps/api   — FastAPI (Python 3.12+)
apps/web   — Next.js 14 App Router + TypeScript + Tailwind
infra/docker-compose.yml — PostgreSQL 16
packages/contracts — placeholder shared types (Stage 2+)
```

## Prasyarat

- Node.js 18+ / npm 10+
- Python 3.11+ (3.12 direkomendasikan)
- Docker Desktop (untuk PostgreSQL)

## Setup (PowerShell)

```powershell
# Clone & branch
git clone https://github.com/7z1x/ai-interviewer.git
cd ai-interviewer
git checkout feat/ai-interviewer-stage-01

# Env
Copy-Item .env.example .env
# Edit .env sesuai kebutuhan (DATABASE_URL, NEXT_PUBLIC_API_URL, dll.)

# Database (Docker)
docker compose -f infra/docker-compose.yml up -d
docker compose -f infra/docker-compose.yml ps
# healthcheck: pg_isready

# Backend
cd apps/api
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8000
# cek: http://localhost:8000/health  -> {status:"ok"}
# docs: http://localhost:8000/docs

# Frontend (terminal baru)
cd apps/web
npm install
$env:NEXT_PUBLIC_API_URL="http://localhost:8000"
npm run dev
# buka: http://localhost:3000  -> status Connected / Loading / Error
```

## Lokasi Runtime

| Service  | Default URL                | Health Check              |
|----------|----------------------------|---------------------------|
| Backend  | http://localhost:8000      | GET /health               |
| Frontend | http://localhost:3000      | halaman menampilkan status|
| Postgres | localhost:5432             | `pg_isready` (docker healthcheck) |

## Quality Gates (PowerShell)

```powershell
# Backend — dari folder apps/api (venv aktif)
ruff check app tests
mypy app
pytest -v
# atau: python -m pytest -v

# Frontend — dari folder apps/web
npm run lint
npm run type-check
npm test
npm run build

# Docker
docker compose -f infra/docker-compose.yml up -d
docker inspect --format="{{.State.Health.Status}}" ai-interviewer-db
# expected: healthy
```

## Endpoint

- `GET /health` → `{status:"ok", service:"ai-interviewer-api", version, timestamp}`

## Catatan Stage 1

- Tidak ada autentikasi, upload CV, LangGraph, interview, voice, avatar, dashboard.
- `.env` di-ignore; commit hanya `.env.example`.
- Test: 1 backend (`GET /health` 200) + 1 frontend (loading→connected / error).
