# IMPLEMENTATION PLAN — AI Interviewer

> Checklist ringkas. Scope dan gate lengkap setiap tahap berada di [`docs/stages/`](stages/README.md). Stage 0 hanya desain — tidak ada kode fitur.

## Prinsip

- Satu hari = satu tahap; jangan loncat tahap.
- Sebelum mulai: `git status`, cek branch `feat/ai-interviewer-stage-XX`, baca `AGENTS.md`, `docs/IMPLEMENTATION_PLAN.md`, `docs/EXECUTION_STATUS.md`, pastikan tahap sebelumnya `verified`.
- Quality gates tiap tahap harus lulus sebelum commit lokal; push hanya jika instruksi eksplisit `PUSH`.
- Stub/deterministik untuk test; jangan bergantung pada API berbayar.

## Stage 0 — Audit and Design [DONE - Stage ini]

- [x] Periksa isi repo, struktur folder, package manager, dan konfigurasi. `AGENTS.md` belum ada saat audit awal dan ditambahkan pada governance follow-up.
- [x] Tentukan: pakai repo existing `7z1x/ai-interviewer` (baru, 1 commit), tidak buat repo/folder baru.
- [x] Buat `docs/PRD.md` (masalah, persona, journey, scope MVP, non-goals, FR, failure states, AC terukur).
- [x] Buat `docs/ARCHITECTURE.md` (batas tanggung jawab, alur data, diagram Mermaid, stub provider, dua mode LLM, error handling & idempotency).
- [x] Dokumentasikan dua mode runtime OpenCode (lokal loopback vs cloud terautentikasi) — perpindahan via konfigurasi.
- [x] Buat `docs/DATA_MODEL.md` (6 entitas + ER diagram + kolom/constraint/index).
- [x] Buat `docs/API_CONTRACT.md` (endpoint, request/response, validation, status code, traceability).
- [x] Buat `docs/IMPLEMENTATION_PLAN.md` (file ini).
- [x] Buat `docs/EXECUTION_STATUS.md`.
- [x] Review desain dan perbaiki governance sebelum Stage 1.

### Governance follow-up [DONE]

- [x] Tambahkan root `AGENTS.md` sebagai aturan utama coding agent.
- [x] Tambahkan `README.md` yang jujur terhadap status project.
- [x] Pisahkan kontrak AI, testing, security/privacy, dan ADR.
- [x] Pecah dokumen prompt menjadi Hermes runbook dan file per stage.
- [x] Kunci batas upload MVP pada 5 MiB dan 10 halaman di dokumen terkait.

**Quality gates**: 4 dokumen desain ada & konsisten, tiap requirement terpetakan ke endpoint+entitas, non-goals eksplisit, tidak ada klaim fitur bekerja.

## Stage 1 — Scaffold and Quality Gates [NEXT PRODUCT STAGE]

- [ ] Scaffold `apps/web` (Next.js TS), `apps/api` (FastAPI), `packages/contracts` atau kontrak sederhana, `infra/docker-compose.yml` (PostgreSQL).
- [ ] `GET /health` terstruktur di backend.
- [ ] Halaman FE sederhana cek health backend (loading/connected/error).
- [ ] `.env.example` + `.gitignore` secret.
- [ ] Scripts: dev, lint, type-check, test, build (BE: Ruff, pytest; FE: Vitest).
- [ ] `README.md` command PowerShell & lokasi runtime.
- [ ] Test: 1 BE health, 1 FE health representation.
- **AC**: BE `/health` 200, FE baca health, lint/type-check/test/build lulus, Postgres container healthy.

## Stage 2 — Database and Session API

- [ ] SQLAlchemy async + Alembic config.
- [ ] Tabel: session, source_document, question, answer, evaluation, final_report (UUID, TIMESTAMPTZ UTC, FK, enum/status).
- [ ] Repository/service layer (route tidak query langsung).
- [ ] Endpoints: POST/GET sessions, GET list, DELETE draft.
- [ ] Migration pertama + seed jika perlu.
- [ ] Integration test DB terisolasi.
- **AC**: migration di DB kosong, CRUD via API, invalid transition ditolak 409, OpenAPI sesuai kontrak.

## Stage 3 — CV Upload and Extraction

- [ ] Validasi MIME, ekstensi, magic bytes, size, page count; path aman (UUID).
- [ ] Ekstrak teks per halaman + metadata `pages[]`.
- [ ] Status `uploaded|processing|ready|failed`; error tidak rusak session.
- [ ] Endpoints upload + status dokumen; cleanup file sementara.
- [ ] Fixture PDF kecil untuk test.
- **AC**: PDF valid → teks/halaman, file palsu/besar/terenkripsi/kosong/rusak ditolak, tanpa path traversal.

## Stage 4 — Candidate Context and Interview Plan

- [ ] Interface `LLMProvider`, `StubLLMProvider`, `OpenCodeProvider` (env: `OPENCODE_BASE_URL`, model, username/password; session terisolasi, tools off, JSON, timeout, cleanup).
- [ ] Pydantic schema structured output; anti-hallucinasi skill.
- [ ] Simpan plan (5 pertanyaan: competency/objective/difficulty/expected_evidence).
- [ ] Endpoint generate plan idempotent + GET plan; health/opencode terpisah.
- [ ] Unit + integration test stub; test tools tidak diberikan ke session.
- **AC**: output invalid di-retry terbatas, plan tersimpan, demo penuh stub tanpa API key, perpindahan lokal↔cloud via env.

## Stage 5 — LangGraph Text Interview

- [ ] State: session_id, status, plan, current index/question, history, follow_up count, remaining, completion_reason.
- [ ] Nodes: load_session, select_question, wait_for_answer, classify_answer, decide_follow_up, persist_turn, advance_or_finish.
- [ ] Aturan: maks 5 utama + 1 follow-up/Q; follow-up jika vague/tidak relevan/butuh evidence; state recoverable; idempotent.
- [ ] Endpoints: start, current-question, answers, next, end.
- [ ] Graph tests: cukup→next, vague→follow-up, batas follow-up, selesai, restart recovery, duplicate dedup.
- **AC**: deterministik stub, state recoverable, batas terjaga.

## Stage 6 — Evidence-based Evaluation

- [ ] Rubric 0–5 (relevance, technical_accuracy, clarity, evidence_specificity, structure), overall hitung kode.
- [ ] Schema ketat + validasi quote substring jawaban.
- [ ] Bedakan jawaban lemah vs provider failure; simpan rubric/prompt version.
- [ ] Endpoints evaluasi per jawaban.
- [ ] Tests: batas skor, quote palsu, output rusak, kosong, retry, persistence.
- **AC**: skor dalam rentang, quote tervalidasi, overall konsisten formula, failure tidak jadi skor 0.

## Stage 7 — Final Report

- [ ] Agregasi numerik via kode; model hanya rangkum evaluasi tervalidasi; provenance (Q/A/Eval IDs).
- [ ] Status `complete|incomplete`; regenerate versioned.
- [ ] Endpoints generate/get report; export JSON.
- [ ] Tests: agregasi, missing eval, provenance, idempotency.
- **AC**: angka tertelusur ke eval, kutipan ke answer, incomplete tidak final, reopen setelah restart.

## Stage 8 — Frontend MVP

- [ ] Halaman: Home/daftar sesi, Setup (upload+role+JD+bahasa+plan), Interview Room, Result Page.
- [ ] Typed API client; loading/empty/error/retry/disabled; cegah double submit; responsive + a11y; tidak simpan CV/key di localStorage.
- [ ] Component tests + E2E happy path stub.
- **AC**: alur setup→interview→report, refresh tidak hilang session, double-click tidak gandakan, lint/type-check/test/build lulus.

## Stage 9 — Observability, Security, Reliability

- [ ] Correlation ID, structured logging, trace LangGraph/provider, Langfuse opsional env (tanpa log CV/JD/jawaban/token).
- [ ] Audit upload, size limit, rate limit AI, timeout/retry, sanitasi error, CORS, ownership boundary, dependency audit, concurrency/duplicate tests, retention policy, TLS+auth OpenCode.
- [ ] Threat model + runbook provider failure.
- **AC**: jalan tanpa Langfuse, trace hanya jika config ada, secret tidak di log, timeout/retry/rate-limit teruji.

## Stage 10 — Voice

- [ ] Decision record: MediaRecorder vs WebSocket/WebRTC, STT/TTS, biaya/latency/i18n/kompleksitas; pilih solusi sederhana teruji.
- [ ] States: requesting_permission, listening, processing, speaking, error; transcript koreksi sebelum submit; stop playback; fallback teks.
- [ ] Provider interface + stub + fixture audio.
- **AC**: voice atau teks, tolak mic tidak blok teks, transcript terlihat sebelum final, error tidak rusak state.

## Stage 11 — Optional Avatar

- [ ] Audit provider avatar (pricing, free-tier, retention, biometric/privacy, browser, fallback); ADR + approval.
- [ ] Adapter, sinkron audio, toggle, fallback statis, isolasi failure, privacy notice.
- **AC**: teks/voice tanpa avatar, failure terisolasi, consent terlihat, biaya dari sumber resmi.

## Stage 12 — Final Verification and Deployment

- [ ] Cocokkan PRD AC (verified/failed/not tested); jalankan dari DB kosong: install, migration, lint/test BE/FE, build, integration, E2E stub.
- [ ] Manual provider nyata jika key ada (jangan minta key).
- [ ] Uji upload error, timeout, refresh, duplicate, incomplete report, DB restart; audit .gitignore/tracked files/log.
- [ ] Buat `docs/DEPLOYMENT.md`, `docs/RUNBOOK.md`, `docs/VERIFICATION_REPORT.md`, `.env.example` final.
- **AC**: report berisi command+output real, blocker jujur, reproducible deploy, secret scan bersih, alur setup→report di staging.

## Dependensi Kritis

```
Stage 0 → 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → (10 → 11) → 12
MVP portfolio terbentuk setelah Stage 9.
```

## Risiko & Mitigasi

| Risiko | Mitigasi |
|---|---|
| OpenCode API tidak stabil/berubah | Adapter terisolasi, contract test, stub fallback |
| Validasi PDF bypass | MIME+magic bytes+page count+size, test fixture palsu |
| Hallucinasi skill/quote | Pydantic + substring validation + rubric versioning |
| State LangGraph hilang saat restart | Persist tiap turn ke DB, load_session recovery test |
