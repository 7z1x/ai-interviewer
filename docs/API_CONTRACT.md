# API CONTRACT — AI Interviewer

> Stage 0 — desain saja. Implementasi endpoint mulai Stage 1. Base URL dev: `http://localhost:8000`.

## 1. Konvensi Umum

- **Base path**: `/api` untuk resource; `/health` untuk liveness tanpa prefix.
- **Auth**: MVP anonymous (tanpa JWT); Stage 9 menambahkan session ownership boundary. Tetap kirim `X-Request-ID` (correlation ID) — jika tidak dikirim, server generate UUID.
- **Content-Type**: `application/json` kecuali upload (`multipart/form-data`).
- **Timestamps**: ISO 8601 UTC `YYYY-MM-DDTHH:mm:ssZ`.
- **ID**: UUID v4 string.
- **Pagination**: `?page=1&page_size=20` (default 20, max 100); response `{items, total, page, page_size}`.
- **Idempotency**: `Idempotency-Key: <uuid>` untuk `POST` yang tidak aman (answers, plan, report). Duplicate key → kembalikan resource existing `200`, tidak buat duplikat.
- **Error envelope** (semua error):
```json
{
  "error": {
    "code": "validation_error | not_found | conflict | payload_too_large | unprocessable | rate_limited | internal",
    "message": "pesan aman untuk client",
    "details": [{"field": "target_role", "issue": "must not be empty"}],
    "request_id": "uuid"
  }
}
```
- **Validation error**: `422` dengan `details[]`; `400` untuk JSON malformed; `413` untuk payload too large; `409` untuk status transition invalid; `429` untuk rate limit.

## 2. Health

### GET /health
Liveness aplikasi (tidak cek OpenCode/DB berat).

- **200**
```json
{"status": "ok", "version": "0.1.0", "uptime_s": 123}
```

### GET /api/health/opencode _(Stage 4)_
Readiness provider — membedakan backend hidup vs OpenCode tersedia.

- **200** `{"status": "reachable", "latency_ms": 42, "model": "openai/gpt-4o-mini"}`
- **503** `{"status": "unreachable", "error": "timeout"}`
- Tidak meneruskan URL/credential ke response.

## 3. Sessions

### POST /api/sessions
Buat draft session.

- **Request**
```json
{
  "target_role": "Backend Engineer",
  "job_description": "Membangun API ...",
  "language": "id"
}
```
Validasi: `target_role` 1–200 char, `job_description` 1–10000 char, `language` enum `id|en`.

- **201**
```json
{
  "id": "uuid",
  "target_role": "Backend Engineer",
  "job_description": "Membangun API ...",
  "language": "id",
  "status": "draft",
  "plan_summary": null,
  "current_question_index": 0,
  "created_at": "2026-09-15T00:00:00Z",
  "updated_at": "2026-09-15T00:00:00Z"
}
```
- **422** jika validasi gagal.

### GET /api/sessions
Daftar sesi terbaru, terurut `created_at DESC`.

- **Query**: `page`, `page_size`, `status` (opsional filter).
- **200**
```json
{
  "items": [{ "id": "uuid", "target_role": "...", "status": "draft", "created_at": "..." }],
  "total": 1, "page": 1, "page_size": 20
}
```

### GET /api/sessions/{sessionId}
Detail session + ringkasan children counts.

- **200** — objek session + `document_status`, `question_count`, `answer_count`, `report_status`.
- **404** jika tidak ditemukan.

### DELETE /api/sessions/{sessionId}
Hapus draft yang belum dimulai.

- **204** jika `status=draft`.
- **409** `{"error": {"code": "conflict", "message": "Only draft sessions can be deleted."}}` jika status lain.
- **404** jika tidak ada.

## 4. Documents (CV Upload)

### POST /api/sessions/{sessionId}/documents
Upload 1 CV PDF per session.

- **Request**: `multipart/form-data` field `file` (PDF). Header opsional `Idempotency-Key`.
- **Validasi**: MIME `application/pdf`, ekstensi `.pdf`, magic bytes `%PDF`, `file_size ≤ 5MB` (konfigurasi), `page_count ≤ 10`, tidak terenkripsi, tidak kosong, tidak rusak.
- **201**
```json
{
  "id": "uuid",
  "session_id": "uuid",
  "original_filename": "cv.pdf",
  "mime_type": "application/pdf",
  "file_size_bytes": 123456,
  "page_count": 2,
  "status": "ready",
  "pages": [{"page_no": 1, "char_count": 1200}],
  "created_at": "..."
}
```
- **413** file terlalu besar.
- **422** `unprocessable` untuk PDF palsu/terenkripsi/kosong/rusak/page count berlebih; `details` berisi `field: file`.
- **409** jika session sudah punya dokumen (satu per session).
- **404** session tidak ada.

### GET /api/sessions/{sessionId}/documents/{documentId}
Status & metadata dokumen (tanpa mengembalikan file biner lagi).

- **200** — objek document seperti di atas + `extracted_text` (opsional, dibatasi) atau `error_message` jika `failed`.
- **404**.

## 5. Interview Plan

### POST /api/sessions/{sessionId}/plan
Generate plan (idempotent). Membutuhkan `SourceDocument status=ready`.

- **Request**: kosong (ambil dari session + document); header `Idempotency-Key` disarankan.
- **Provider**: `LLMProvider.generatePlan(cvText, role, jd, lang)` → validasi Pydantic (tepat 5 pertanyaan, competency/objective wajib, skills hanya dari CV).
- **201** (baru dibuat)
```json
{
  "session_id": "uuid",
  "profile_summary": "Kandidat 5 tahun ...",
  "skills_found": ["Python", "FastAPI"],
  "job_requirements": ["Python", "PostgreSQL"],
  "fit": ["..."],
  "gaps": ["..."],
  "questions": [
    {
      "id": "uuid", "order_index": 0, "question_text": "...",
      "competency": "problem_solving", "objective": "...",
      "difficulty": "medium", "expected_evidence": "...", "kind": "main"
    }
  ]
}
```
- **200** jika idempotency key sama / plan sudah ada dan regenerate tidak diminta.
- **422** jika output provider invalid (retry terbatas lalu 502/503 internal sanitized).
- **409** jika session status tidak memungkinkan.
- **404** session/document tidak ada.

### GET /api/sessions/{sessionId}/plan
Ambil plan tersimpan.

- **200** — payload sama.
- **404** jika belum ada.

## 6. Interview (LangGraph)

### POST /api/sessions/{sessionId}/interview/start
Mulai interview.

- **201** `{"status": "in_progress", "current_question_index": 0}`
- **409** jika sudah `in_progress`/`completed`.
- **422** jika belum punya plan.

### GET /api/sessions/{sessionId}/interview/current-question
Pertanyaan aktif.

- **200**
```json
{
  "question": {"id": "uuid", "order_index": 0, "question_text": "...", "competency": "...", "objective": "...", "difficulty": "medium", "expected_evidence": "...", "kind": "main", "parent_question_id": null},
  "progress": {"current": 1, "total": 5, "follow_up_used": 0, "follow_up_limit": 1},
  "status": "in_progress"
}
```
- **200** `{"status": "completed", "question": null}` jika selesai.
- **404** session tidak ada.

### POST /api/sessions/{sessionId}/interview/answers
Kirim jawaban untuk pertanyaan aktif.

- **Request**
```json
{"question_id": "uuid", "answer_text": "Saya pernah ...", "idempotency_key": "uuid-opsional"}
```
Header alternatif: `Idempotency-Key`.

- **201** `{"id": "uuid", "question_id": "uuid", "answer_text": "...", "submitted_at": "..."}`
- **200** jika duplicate `Idempotency-Key` / `question_id` sudah dijawab — kembalikan jawaban existing.
- **400** `answer_text` kosong.
- **409** interview belum `in_progress` atau sudah `completed`.
- **422** `question_id` tidak match pertanyaan aktif.

### POST /api/sessions/{sessionId}/interview/next
Lanjut ke pertanyaan berikutnya (dipanggil setelah evaluasi/follow-up decision).

- **200** — `{"current_question_index": 1, "status": "in_progress"}` atau `{"status": "completed"}` jika sudah habis (5 utama + follow-up).
- **409** jika tidak ada jawaban untuk pertanyaan aktif.

### POST /api/sessions/{sessionId}/interview/end
Akhiri interview manual.

- **200** `{"status": "completed", "completion_reason": "user_ended | all_questions_done"}`

## 7. Evaluation

### POST /api/sessions/{sessionId}/answers/{answerId}/evaluation
Evaluasi satu jawaban (idempotent).

- **Request**: kosong (ambil answer_text + question); header `Idempotency-Key`.
- **201**
```json
{
  "id": "uuid", "answer_id": "uuid", "session_id": "uuid", "question_id": "uuid",
  "relevance": 4, "technical_accuracy": 3, "clarity": 4, "evidence_specificity": 3, "structure": 4,
  "overall": 3.6, "rationale": "...", "evidence_quote": "substring persis dari jawaban",
  "strengths": ["..."], "improvements": ["..."], "confidence": 0.82,
  "status": "evaluated", "rubric_version": "v1.0", "prompt_version": "v1.0"
}
```
Validasi: `evidence_quote` harus substring `answer_text`; skor 0–5; `overall` dihitung kode.

- **200** jika sudah ada (idempotent).
- **422** jika answer kosong / insufficient → `status: insufficient_answer`.
- **502/503** sanitized jika provider gagal (tidak simpan skor 0 palsu).
- **404**.

### GET /api/sessions/{sessionId}/answers/{answerId}/evaluation
Ambil evaluasi.

- **200** — objek evaluation.
- **404** jika belum ada.

## 8. Report

### POST /api/sessions/{sessionId}/report
Generate final report (idempotent, versioned).

- **201**
```json
{
  "id": "uuid", "session_id": "uuid", "status": "complete",
  "summary": "...", "scores_per_competency": {"problem_solving": 3.8},
  "overall_score": 3.6, "strengths": ["..."], "improvements": ["top 3"],
  "recommendations": ["..."],
  "question_evaluations": [{"question_id": "uuid", "answer_id": "uuid", "evaluation_id": "uuid"}],
  "provenance": {"question_ids": ["uuid"], "answer_ids": ["uuid"], "evaluation_ids": ["uuid"], "rubric_version": "v1.0"},
  "disclaimer": "Laporan adalah alat latihan, bukan keputusan hiring.",
  "version": 1, "created_at": "..."
}
```
- **200** jika duplicate key / sudah ada versi yang sama.
- **200** `{"status": "incomplete", "missing": ["evaluation for q3"]}` jika evaluasi belum lengkap — tidak dipresentasikan sebagai final.
- **404**.

### GET /api/sessions/{sessionId}/report
Ambil report terbaru (atau `?version=1`).

- **200** — objek report.
- **404** jika belum ada.

## 9. Status Code Ringkas

| Code | Makna | Dipakai Untuk |
|---|---|---|
| 200 | OK | GET, duplicate idempotent POST |
| 201 | Created | POST create pertama |
| 204 | No Content | DELETE sukses |
| 400 | Bad Request | JSON malformed, answer_text kosong |
| 404 | Not Found | session/document/question/answer/report tidak ada |
| 409 | Conflict | status transition invalid, sudah punya document/plan |
| 413 | Payload Too Large | file > batas |
| 422 | Unprocessable | validasi business / PDF parse / provider invalid output |
| 429 | Too Many Requests | rate limit endpoint AI (Stage 9) |
| 500 | Internal | error tak terduga (sanitized) |
| 502/503 | Bad Gateway / Unavailable | provider unreachable (sanitized) |

## 10. Traceability Matrix (Requirement → Endpoint → Entitas)

| Requirement | Endpoint | Entitas |
|---|---|---|
| FR-01 | POST /api/sessions | InterviewSession |
| FR-02 | GET /api/sessions, GET /api/sessions/{id} | InterviewSession |
| FR-03 | DELETE /api/sessions/{id} | InterviewSession |
| FR-04 | POST .../documents, GET .../documents/{id} | SourceDocument |
| FR-05 | POST .../plan, GET .../plan | InterviewQuestion |
| FR-06 | POST .../interview/start, GET .../current-question, POST .../answers, POST .../next, POST .../end | InterviewSession/Q/A |
| FR-07 | internal classify/decide (via POST answers + next) | CandidateAnswer |
| FR-08 | POST .../answers/{id}/evaluation | AnswerEvaluation |
| FR-09 | POST .../report, GET .../report | FinalReport |
| FR-10 | GET /health, GET /api/health/opencode | — |

## 11. Catatan Keamanan

- Upload: jangan percaya `original_filename` untuk path; simpan dengan UUID; bersihkan file sementara.
- CORS: hanya origin yang dikonfigurasi (Stage 9).
- Tidak meneruskan `OPENCODE_BASE_URL` / credential ke frontend.
- `.env` dan CV tidak di-commit; `.env.example` berisi nama variabel saja.
