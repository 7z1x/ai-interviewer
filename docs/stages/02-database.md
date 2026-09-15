# Stage 2 — Database and Session API

## Scope

Implementasikan persistence dan lifecycle session sesuai `../DATA_MODEL.md`, `../API_CONTRACT.md`, dan keputusan ownership yang sudah difinalkan.

## Deliverables

- SQLAlchemy async dan Alembic.
- Enam tabel minimum dengan UUID, UTC timestamps, FK, constraint, dan status jelas.
- Repository/service layer; route tidak query langsung.
- Create, detail, list, dan delete-draft session endpoint.
- Integration test dengan database terisolasi.

## Do Not Build

AI, upload, LangGraph, scoring, voice, atau avatar.

## Gate

Migration berjalan dari database kosong, CRUD terbukti melalui API, invalid transition ditolak, ownership boundary diuji, dan OpenAPI sesuai contract.
