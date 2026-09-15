# Stage 1 — Scaffold and Quality Gates

## Scope

Buat fondasi project saja: `apps/web`, `apps/api`, kontrak bersama yang paling sederhana, dan PostgreSQL lokal melalui Docker Compose.

## Deliverables

- Next.js TypeScript frontend dan FastAPI Python 3.12 backend.
- `GET /health` terstruktur.
- Halaman frontend dengan state loading, connected, dan error untuk health backend.
- `.gitignore`, `.env.example`, command development, format/lint, typecheck, test, dan build.
- README diperbarui dengan command PowerShell aktual.
- Satu test backend dan satu test frontend untuk health flow.

## Do Not Build

Authentication, upload CV, LangGraph, interview, scoring, voice, avatar, atau dashboard.

## Gate

Backend/frontend dapat start; `/health` mengembalikan 200; PostgreSQL sehat; seluruh quality gate aktual lulus.
