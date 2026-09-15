# Testing Strategy — AI Interviewer

> Dokumen ini menentukan bukti yang dibutuhkan. Command konkret ditambahkan pada Stage 1 setelah package dan tool benar-benar tersedia.

## 1. Prinsip

- Automated test default tidak boleh membutuhkan API AI berbayar, internet, atau credential.
- Gunakan `StubLLMProvider` yang deterministik untuk unit, integration, graph, dan E2E test utama.
- Setiap bug fix harus mempunyai regression test pada layer terdekat dengan penyebabnya.
- Test tidak boleh bergantung pada urutan eksekusi, waktu lokal, atau data pengguna asli.
- Lint, typecheck, build, dan runtime test adalah bukti yang berbeda.

## 2. Quality Gate Matrix

| Jenis perubahan | Bukti minimum |
|---|---|
| Dokumentasi/contract | link check, consistency review, diff review |
| Frontend component | format, lint, typecheck, component test |
| Frontend route/data flow | seluruh gate component + production build + route/E2E check |
| Backend domain/service | Ruff format/check, Python typecheck, unit test |
| API endpoint | gate backend + integration test + OpenAPI/response contract check |
| Database schema | migration upgrade dari DB kosong + constraint dan repository integration test |
| Upload PDF | valid, MIME mismatch, magic-byte mismatch, oversize, page-limit, encrypted, empty, corrupt, cleanup |
| LangGraph | transition tests, limit tests, duplicate submission, persistence/recovery |
| Provider adapter | mocked HTTP contract tests; live smoke test dipisahkan dan opsional |
| Prompt/model/schema/rubric | structured-output tests + versioned AI evaluation regression |
| Full MVP | E2E setup → interview → report dalam stub mode |

## 3. Test Layers

### Unit

Menguji fungsi murni, validation, scoring formula, status transition, evidence matching, dan mapping provider tanpa database/network nyata.

### Integration

Menguji route, service, repository, migration, database constraint, dan mocked provider boundary. Database test harus terisolasi dan dapat dibuat ulang.

### Graph

Minimal mencakup:

- jawaban cukup menuju pertanyaan utama berikutnya;
- jawaban vague menghasilkan satu follow-up;
- batas follow-up tidak terlewati;
- lima pertanyaan menyelesaikan interview;
- restart memulihkan state;
- idempotency key yang sama tidak menggandakan answer/turn.

### End-to-End

Happy path utama memakai stub: buat session, upload fixture PDF, generate plan, selesaikan interview, generate report, refresh, lalu buka report kembali.

### Live Provider Smoke Test

Dijalankan terpisah dan hanya jika environment telah dikonfigurasi oleh pengguna. Hasilnya tidak menjadi bagian test default dan tidak boleh menampilkan credential atau isi CV pengguna.

## 4. AI Evaluation

Dataset dan expected result harus versioned. Pisahkan:

- deterministic contract evaluation: schema, range, exact quote, formula, limits;
- quality evaluation: relevance, follow-up decision, feedback usefulness, hallucination rate;
- operational evaluation: latency, error rate, retry rate, dan cost.

Perubahan prompt/model tidak lulus hanya karena schema valid. Bandingkan terhadap baseline dan laporkan regression, improvement, serta sample yang masih gagal.

## 5. Required Failure Cases

- provider timeout, unavailable, rate-limited, malformed JSON, dan output di luar schema;
- database unavailable atau restart saat session aktif;
- duplicate request dan concurrent submission;
- invalid status transition;
- report ketika evaluation belum lengkap;
- refresh frontend pada setiap status utama;
- OpenCode unavailable sementara backend tetap live;
- Langfuse tidak dikonfigurasi;
- file upload berbahaya atau tidak valid.

## 6. CI Policy

Setelah Stage 1 membuat toolchain, CI pull request minimal menjalankan:

1. secret/config safety check;
2. frontend format, lint, typecheck, test, build;
3. backend format check, lint, typecheck, test;
4. migration smoke test pada PostgreSQL kosong;
5. E2E stub setelah alur tersedia.

Command di CI dan README harus merujuk script yang benar-benar ada. Jangan mendokumentasikan command fiktif.

## 7. Reporting Results

Setiap laporan verifikasi mencatat command persis, exit code/ringkasan hasil, environment penting, test yang belum dijalankan, dan blocker. Kata `verified` hanya digunakan jika acceptance criteria terkait mempunyai bukti.
