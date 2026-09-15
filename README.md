# AI Interviewer

Portfolio project untuk latihan interview kerja berbasis AI. Pengguna akan mengunggah CV PDF, memasukkan target role dan job description, menjalani interview teks adaptif, lalu menerima evaluasi berbasis rubric dan kutipan jawaban.

## Status

Stage 1 — Scaffold and Quality Gates selesai (verified). Stage 0 desain juga verified. `ai-interviewer-db` PostgreSQL healthy. Status eksekusi terkini di [`docs/EXECUTION_STATUS.md`](docs/EXECUTION_STATUS.md).

## MVP

- Upload satu CV PDF dan ekstraksi text layer per halaman.
- Membuat interview plan dari CV, target role, dan job description.
- Interview teks adaptif dengan maksimal lima pertanyaan utama dan satu follow-up per pertanyaan.
- Evaluasi terstruktur dengan evidence quote dari jawaban kandidat.
- Final report yang dapat ditelusuri kembali ke pertanyaan, jawaban, dan evaluasi.
- Persistensi sesi agar interview dapat dilanjutkan setelah refresh atau restart.

Voice, avatar, OCR, live coding, admin panel, dan billing bukan bagian MVP.

## Planned Stack

- Web: Next.js App Router, TypeScript, Tailwind CSS.
- API: Python 3.12, FastAPI, Pydantic.
- Workflow: LangGraph.
- Database: PostgreSQL, SQLAlchemy 2, Alembic.
- AI gateway: OpenCode HTTP server melalui provider adapter.
- Tests: pytest, Vitest, Testing Library.
- Local infrastructure: Docker Compose.

## Struktur

```
apps/api   — FastAPI (Python 3.12+)
apps/web   — Next.js 14 App Router + TypeScript + Tailwind
infra/docker-compose.yml — PostgreSQL 16 (ai-interviewer-db, healthy)
packages/contracts — placeholder shared types (Stage 2+)
```

## Documentation

- [`AGENTS.md`](AGENTS.md) — aturan kerja untuk coding agent.
- [`docs/PRD.md`](docs/PRD.md) — scope, requirement, dan acceptance criteria produk.
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — batas komponen dan alur data.
- [`docs/DATA_MODEL.md`](docs/DATA_MODEL.md) — entitas, relasi, dan constraint.
- [`docs/API_CONTRACT.md`](docs/API_CONTRACT.md) — kontrak endpoint.
- [`docs/AI_SYSTEM.md`](docs/AI_SYSTEM.md) — kontrak provider, validasi, dan evaluasi AI.
- [`docs/TESTING.md`](docs/TESTING.md) — strategi serta quality gates.
- [`docs/SECURITY.md`](docs/SECURITY.md) — keamanan, privasi, dan retensi data.
- [`docs/GIT_CONVENTION.md`](docs/GIT_CONVENTION.md) — konvensi branch/commit/PR.
- [`docs/IMPLEMENTATION_PLAN.md`](docs/IMPLEMENTATION_PLAN.md) — urutan stage.
- [`docs/EXECUTION_STATUS.md`](docs/EXECUTION_STATUS.md) — checkpoint terakhir yang terverifikasi.
- [`docs/HERMES_RUNBOOK.md`](docs/HERMES_RUNBOOK.md) — cara menjalankan satu stage melalui Hermes.
- [`docs/stages/README.md`](docs/stages/README.md) — indeks instruksi setiap stage.

## Prasyarat

- Node.js 18+ / npm 10+
- Python 3.11+ (3.12 direkomendasikan)
- Docker (untuk PostgreSQL — sudah terverifikasi healthy)

## Setup (PowerShell)

```powershell
# Clone
git clone https://github.com/7z1x/ai-interviewer.git
cd ai-interviewer

# Env
Copy-Item .env.example .env
# Edit .env sesuai kebutuhan (DATABASE_URL, NEXT_PUBLIC_API_URL, dll.)

# Database (Docker)
docker compose -f infra/docker-compose.yml up -d
docker compose -f infra/docker-compose.yml ps
# healthcheck: pg_isready — expected healthy
sg docker -c "docker inspect --format='{{.State.Health.Status}}' ai-interviewer-db"

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
| Postgres | localhost:5432             | `pg_isready` (docker healthcheck) — healthy |

## Quality Gates (PowerShell)

```powershell
# Backend — dari folder apps/api (venv aktif)
ruff check app tests
mypy app
pytest -v

# Frontend — dari folder apps/web
npm run lint
npm run type-check
npm test
npm run build

# Docker
sg docker -c "docker compose -f infra/docker-compose.yml up -d"
sg docker -c "docker inspect --format='{{.State.Health.Status}}' ai-interviewer-db"
# expected: healthy
```

## Endpoint

- `GET /health` → `{status:"ok", service:"ai-interviewer-api", version, timestamp}`

## Catatan Stage 1

- Tidak ada autentikasi, upload CV, LangGraph, interview, voice, avatar, dashboard.
- `.env` di-ignore; commit hanya `.env.example`.
- Test: 1 backend (`GET /health` 200) + 1 frontend (loading→connected / error).
- Branch convention: `feat/<feature-kebab>` — Stage N di commit body, bukan title. Lihat `docs/GIT_CONVENTION.md`.

## Working Agreement

Sebelum mengubah project, baca [`AGENTS.md`](AGENTS.md), dokumen desain yang relevan, dan execution status. Kerjakan satu stage dalam satu waktu dan jangan menandai stage selesai tanpa bukti acceptance criteria.
