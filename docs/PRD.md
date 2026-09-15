# PRD — AI Interviewer

> Stage 0 — Audit dan Rancangan Awal. Dokumen desain saja; tidak ada klaim fitur sudah bekerja.

## 1. Ringkasan Eksekutif

AI Interviewer adalah aplikasi latihan interview berbasis AI untuk membantu kandidat mempersiapkan interview kerja. Pengguna mengunggah CV PDF, memasukkan job description dan target role, lalu menjalani interview adaptif berbasis teks. Sistem menilai setiap jawaban dengan rubric terstruktur dan bukti kutipan jawaban, lalu menghasilkan laporan akhir yang dapat dibuka kembali.

Status repo saat Stage 0: repository baru, 1 commit di `main` (`80487d3 docs: add AI Interviewer step-by-step prompts`), working tree clean, belum ada kode aplikasi, scaffold, atau dependency.

## 2. Masalah Pengguna

1. Kandidat kesulitan berlatih interview yang relevan dengan CV dan lowongan spesifik; latihan generik tidak memberi feedback actionable.
2. Kandidat tidak mendapat penilaian terstruktur (relevance, technical accuracy, clarity, evidence, structure) dengan bukti kutipan — feedback mentor tidak skalabel.
3. Kandidat tidak punya rekam jejak sesi latihan yang dapat dibuka ulang untuk melihat progress.

## 3. Persona

| Persona | Deskripsi | Kebutuhan Utama |
|---|---|---|
| **Fresh Graduate** | Baru lulus, CV tipis, belum pernah interview formal | Pertanyaan yang menggali proyek/skripsi, feedback struktur jawaban STAR |
| **Mid-level Switcher** | 3–7 tahun pengalaman, pindah role/stack | Pertanyaan yang memetakan skill CV vs requirement JD, gap analysis |
| **Career Returner** | Jeda karir, perlu percaya diri | Latihan berulang, laporan strengths/improvements yang memotivasi |

Non-persona MVP: recruiter, hiring manager, admin — tidak ada role terpisah di MVP.

## 4. User Journey

### Journey Utama (Happy Path)
1. User membuka Home → melihat daftar sesi sebelumnya.
2. User klik "New Session" → isi `target_role`, `job_description`, pilih `language` (id/en).
3. User upload CV PDF (1 file, maksimum 5 MiB dan 10 halaman) → sistem ekstrak teks per halaman → status `ready`.
4. User klik "Generate Interview Plan" → sistem memanggil provider AI → menghasilkan ringkasan profil, skills dari CV, requirement JD, fit/gap, dan 5 pertanyaan awal (competency, objective, difficulty, expected_evidence) → simpan ke DB.
5. User klik "Start Interview" → masuk Interview Room, melihat pertanyaan 1/5, progress bar.
6. User mengetik jawaban → submit → sistem klasifikasi jawaban → jika jawaban vague/tidak relevan → 1 follow-up; jika cukup → lanjut pertanyaan berikutnya. Maks 5 utama + maks 1 follow-up per pertanyaan utama.
7. User menyelesaikan atau mengakhiri interview → sistem mengevaluasi setiap jawaban dengan rubric 0–5 + evidence quote (substring jawaban).
8. User membuka Result Page → melihat overall score (dihitung kode), skor per dimensi/competency, strengths, top 3 improvements, rekomendasi latihan, evidence quote per jawaban, disclaimer latihan.
9. User membuka kembali sesi/report kapan saja dari daftar sesi.

### Journey Alternatif / Error
- Upload gagal (file palsu/engkripsi/kosong/rusak/terlalu besar) → pesan aman, session tetap draft.
- Provider timeout/invalid output → retry terbatas, tidak simpan skor nol palsu.
- Refresh saat interview → state dipulihkan dari DB.
- Duplicate submit (double-click) → idempotent, tidak gandakan turn.

## 5. Scope MVP

**In:**
- Upload 1 CV PDF per session (maksimum 5 MiB dan 10 halaman), ekstraksi teks per halaman (text layer saja, tanpa OCR).
- Input target_role, job_description, language.
- Generate interview plan 5 pertanyaan via LLM provider (stub + OpenCode).
- LangGraph workflow interview teks (5 utama + 1 follow-up/pertanyaan), persist state.
- Evaluation engine evidence-based (5 dimensi 0–5, overall hitung kode, quote validasi substring).
- Final report agregat (skor, strengths, improvements, rekomendasi, provenance).
- Sesi dan hasil dapat dibuka kembali.
- Frontend MVP: Home/daftar sesi, Setup, Interview Room, Result Page.

**Out — Non-Goals (Eksplisit):**
- Voice interview, STT/TTS, avatar (Stage 10–11, bukan MVP).
- Live coding / editor kode.
- Admin panel, role/permission, multi-tenant.
- Production billing / payment / subscription.
- Embeddings / RAG perusahaan, OCR, export PDF (kecuali disetujui kemudian).
- Authentication penuh (MVP anonymous dengan session ownership boundary sederhana di Stage 9).

## 6. Functional Requirements

| ID | Requirement | Pemetaan Endpoint | Pemetaan Entitas |
|---|---|---|---|
| FR-01 | Buat draft session dengan target_role, JD, language | `POST /api/sessions` | InterviewSession |
| FR-02 | Lihat daftar & detail session | `GET /api/sessions`, `GET /api/sessions/{id}` | InterviewSession |
| FR-03 | Hapus draft yang belum dimulai | `DELETE /api/sessions/{id}` | InterviewSession |
| FR-04 | Upload 1 CV PDF per session, validasi & ekstrak per halaman | `POST /api/sessions/{id}/documents`, `GET .../documents/{docId}` | SourceDocument |
| FR-05 | Generate interview plan (profil, skills CV, requirement JD, fit/gap, 5 pertanyaan) | `POST /api/sessions/{id}/plan`, `GET /api/sessions/{id}/plan` | InterviewQuestion (+ derived context simpan di InterviewSession/JSON) |
| FR-06 | Jalankan interview teks adaptif (start, current question, submit answer, next, end) | `POST .../interview/start`, `GET .../interview/current-question`, `POST .../interview/answers`, `POST .../interview/next`, `POST .../interview/end` | InterviewSession, InterviewQuestion, CandidateAnswer |
| FR-07 | Klasifikasi jawaban & keputusan follow-up (maks 1/pertanyaan) | Internal LangGraph nodes `classify_answer` → `decide_follow_up` | CandidateAnswer, InterviewQuestion |
| FR-08 | Evaluasi per jawaban (5 dimensi, overall hitung kode, quote substring, status) | `POST /api/sessions/{id}/answers/{aid}/evaluation`, `GET ...` | AnswerEvaluation |
| FR-09 | Generate & tampilkan final report (agregasi kode, provenance, disclaimer) | `POST /api/sessions/{id}/report`, `GET /api/sessions/{id}/report` | FinalReport |
| FR-10 | Health check | `GET /health`, `GET /api/health/opencode` (Stage 4) | — |
| FR-11 | Persistensi & recovery state interview setelah restart | Semua endpoint read mengembalikan state dari DB | Semua entitas |
| FR-12 | Idempotency untuk submit jawaban & generate plan/report | Header `Idempotency-Key` / dedup key | CandidateAnswer, InterviewQuestion, FinalReport |

Setiap requirement MVP memiliki endpoint dan entitas — traceability terpenuhi.

## 7. Failure States

| Kondisi Gagal | Perilaku Sistem | Pesan ke User |
|---|---|---|
| PDF palsu (MIME/signature mismatch) | Tolak 422, status `failed`, session tetap draft | "File ditolak: format tidak valid. Hanya PDF." |
| PDF terlalu besar / halaman > batas | Tolak 413/422 | "File terlalu besar / terlalu banyak halaman." |
| PDF terenkripsi / kosong / rusak | Tolak 422, error category `parse_error` | "PDF tidak dapat diproses." |
| Teks CV kosong setelah ekstraksi | Tandai `failed`, tidak lanjut ke plan | "Teks tidak ditemukan di PDF." |
| Provider invalid JSON / out-of-range score | Retry terbatas, lalu gagal tanpa simpan evaluasi sukses | "Gagal menghasilkan plan/evaluasi, coba lagi." |
| Provider timeout | Timeout + retry terbatas, log latency/error category | "Layanan AI lambat, coba lagi." |
| Evidence quote bukan substring jawaban | Tolak evaluasi, status `needs_review` | Tidak tampil sebagai `evaluated` |
| Session status transition invalid | 409 Conflict | "Aksi tidak valid untuk status saat ini." |
| Duplicate submit | Kembalikan resource existing, 200 | Tidak ada duplikasi turn |
| DB restart | State dipulihkan dari DB | User lanjutkan sesi |
| Langfuse tidak dikonfigurasi | Aplikasi tetap jalan, trace dinonaktifkan | Tidak ada error user |

Semua error ke client disanitasi — tidak membocorkan path, stack trace, atau credential.

## 8. Acceptance Criteria Terukur

| ID | Kriteria | Cara Ukur |
|---|---|---|
| AC-01 | User dapat menyelesaikan alur setup → interview (5 Q) → report dalam stub mode tanpa API key | E2E test + manual happy path |
| AC-02 | PDF valid → teks per halaman terekstrak, metadata halaman tersimpan | Unit + integration test upload |
| AC-03 | File palsu/besar/terenkripsi/kosong/rusak ditolak dengan status 4xx yang benar | Test validasi upload |
| AC-04 | Plan berisi tepat 5 pertanyaan, masing-masing punya competency + objective | Unit test provider schema |
| AC-05 | Interview tidak melebihi 5 utama + 1 follow-up/pertanyaan | Graph test |
| AC-06 | Follow-up hanya muncul jika jawaban vague/tidak relevan/butuh evidence | Graph test klasifikasi |
| AC-07 | Setiap evaluasi punya 5 skor 0–5, overall = hitung kode sesuai bobot terdokumentasi | Test formula |
| AC-08 | Evidence quote tervalidasi substring jawaban; quote palsu ditolak | Test validasi quote |
| AC-09 | Report angka tertelusur ke evaluation; kutipan tertelusur ke answer | Test provenance |
| AC-10 | Refresh tidak kehilangan session; duplicate submit tidak gandakan turn | Test persistence & idempotency |
| AC-11 | Lint, type-check, test, build lulus di backend & frontend | CI quality gates |
| AC-12 | Tidak ada secret/CV di log, repo, atau localStorage | Secret scan + log audit |

## 9. Keputusan Audit Repo (Historical Stage 0 Snapshot)

- Repo `7z1x/ai-interviewer` baru (1 commit), belum ada scaffold — keputusan: **pakai repo yang ada**, tidak membuat repo/folder baru, tidak mencampur dengan aplikasi tidak relevan.
- Saat Stage 0 belum ada `AGENTS.md`; root `AGENTS.md` kemudian ditambahkan pada governance follow-up dan sekarang menjadi aturan utama.
- Branch Stage 0: `feat/ai-interviewer-stage-00` (sesuai kontrak `feat/ai-interviewer-stage-XX`).
- Stack terkunci dipatuhi mulai Stage 1; Stage 0 tidak menambah dependency/migration/endpoint/UI.

## 10. Konvensi Git — Branch, Commit, PR (Wajib)

> Revisi 2026-09-15: Penamaan `feat(stage-N)` dihentikan.

### Branch
- Format: `feat/<feature-kebab>` — bukan `feat/ai-interviewer-stage-XX`
- Contoh: `feat/scaffold`, `feat/db-session`, `feat/cv-upload`, `feat/interview-plan`, `feat/interview-graph`, `feat/evaluation`, `feat/report`, `feat/frontend-mvp`, `feat/observability`
- Untuk bugfix setelah merge: `fix/<feature>-<issue-kebab>` contoh `fix/db-migration-uuid`

### Commit
- Format: `feat(<scope>): <deskripsi imperatif>` atau `fix(<scope>): <deskripsi>`
- `<scope>` = fitur (`scaffold`, `db`, `upload`, `agent`, `interview`, `evaluation`, `report`, `web`, `infra`), BUKAN `stage-1`
- Stage number ditaruh di body commit, bukan di title
- Contoh:
  ```
  feat(scaffold): init Next.js + FastAPI + postgres health check

  Stage 1 — Scaffold and Quality Gates
  Docs: PRD.md, ARCHITECTURE.md
  ```
  ```
  feat(db): session and document tables with Alembic migration

  Stage 2 — Database and Session API
  Closes Stage 2 AC-01..05
  ```

### Pull Request
- Title: sama dengan commit title `feat(<scope>): <deskripsi>` — JANGAN pakai `feat(stage-N)`
- Description WAJIB berisi:
  - `Stage N — <Nama Tahap>` 
  - Link ke `docs/AI_INTERVIEWER_STEP_BY_STEP_PROMPTS.md#Prompt N`
  - Checklist acceptance criteria
  - Command yang dijalankan + hasil
- Label: `stage-N` jika perlu, tapi title tetap feature-based

