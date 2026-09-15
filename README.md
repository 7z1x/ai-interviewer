# AI Interviewer

Portfolio project untuk latihan interview kerja berbasis AI. Pengguna akan mengunggah CV PDF, memasukkan target role dan job description, menjalani interview teks adaptif, lalu menerima evaluasi berbasis rubric dan kutipan jawaban.

## Status

Project masih berada pada fase desain. Stage 0 sudah selesai; source code aplikasi, dependency, endpoint, database, dan UI belum dibuat. Status eksekusi terkini berada di [`docs/EXECUTION_STATUS.md`](docs/EXECUTION_STATUS.md).

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

## Documentation

- [`AGENTS.md`](AGENTS.md) — aturan kerja untuk coding agent.
- [`docs/PRD.md`](docs/PRD.md) — scope, requirement, dan acceptance criteria produk.
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — batas komponen dan alur data.
- [`docs/DATA_MODEL.md`](docs/DATA_MODEL.md) — entitas, relasi, dan constraint.
- [`docs/API_CONTRACT.md`](docs/API_CONTRACT.md) — kontrak endpoint.
- [`docs/AI_SYSTEM.md`](docs/AI_SYSTEM.md) — kontrak provider, validasi, dan evaluasi AI.
- [`docs/TESTING.md`](docs/TESTING.md) — strategi serta quality gates.
- [`docs/SECURITY.md`](docs/SECURITY.md) — keamanan, privasi, dan retensi data.
- [`docs/IMPLEMENTATION_PLAN.md`](docs/IMPLEMENTATION_PLAN.md) — urutan stage.
- [`docs/EXECUTION_STATUS.md`](docs/EXECUTION_STATUS.md) — checkpoint terakhir yang terverifikasi.
- [`docs/HERMES_RUNBOOK.md`](docs/HERMES_RUNBOOK.md) — cara menjalankan satu stage melalui Hermes.
- [`docs/stages/README.md`](docs/stages/README.md) — indeks instruksi setiap stage.

## Development

Command install, development, lint, typecheck, test, build, database, dan environment akan ditambahkan pada Stage 1 setelah scaffold benar-benar tersedia. Dokumen ini sengaja tidak menampilkan command yang belum dapat dijalankan.

Jangan memasukkan API key atau credential ke repository. Gunakan `.env.example` sebagai kontrak konfigurasi setelah Stage 1 membuatnya.

## Working Agreement

Sebelum mengubah project, baca [`AGENTS.md`](AGENTS.md), dokumen desain yang relevan, dan execution status. Kerjakan satu stage dalam satu waktu dan jangan menandai stage selesai tanpa bukti acceptance criteria.
