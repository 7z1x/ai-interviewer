# Step-by-Step Prompt: AI Interviewer Portfolio Project

Dokumen ini dipakai **berurutan**. Jangan kirim semua prompt sekaligus. Kirim satu prompt kepada AI executor, tunggu implementasi dan bukti pengujian, lalu lanjut ke tahap berikutnya.

## Cara Menjalankan dengan Hermes melalui WhatsApp

Dokumen ini berada di komputer pengguna. Hermes yang berjalan di server/cloud **tidak dapat membaca path Windows `G:\...` secara langsung**. Sebelum menjalankan tahap pertama:

1. Buat repository GitHub khusus untuk AI Interviewer.
2. Masukkan dokumen ini ke repository tersebut, misalnya sebagai `docs/AI_INTERVIEWER_STEP_BY_STEP_PROMPTS.md`.
3. Pastikan Hermes mengetahui URL repository dan working directory hasil clone di runtime Hermes.
4. Jangan mengirim GitHub token, API key, password, atau isi `.env` melalui WhatsApp. Credential harus sudah tersedia di secret store/runtime Hermes.
5. Kirim **Prompt Kontrol Harian** di bawah ini, bukan hanya pesan seperti "lanjutkan project".

Isi placeholder ini sebelum eksekusi pertama:

```text
REPOSITORY_URL=<URL repository GitHub AI Interviewer>
DEFAULT_BRANCH=<nama default branch, misalnya main>
WORKING_DIRECTORY=<path checkout repository di runtime Hermes>
PROMPT_DOCUMENT=docs/AI_INTERVIEWER_STEP_BY_STEP_PROMPTS.md
```

### Kontrak Eksekusi Harian Hermes

Hermes wajib mengikuti aturan berikut pada setiap hari pengerjaan:

- Kerjakan tepat **satu tahap** yang diminta pengguna. Jangan otomatis masuk tahap berikutnya.
- Sebelum mengedit, jalankan `git status`, periksa branch aktif, baca `AGENTS.md`, dokumen desain, `docs/IMPLEMENTATION_PLAN.md`, dan `docs/EXECUTION_STATUS.md`.
- Pastikan tahap sebelumnya berstatus `verified`. Jika belum, perbaiki/verifikasi tahap sebelumnya dalam scope hari itu dan jangan mulai tahap baru.
- Tarik perubahan remote hanya jika working tree aman. Jangan memakai force push, `git reset --hard`, atau menghapus perubahan yang tidak dipahami.
- Gunakan branch fitur `feat/ai-interviewer-stage-XX` kecuali pengguna secara eksplisit menentukan branch lain.
- Satu hari berarti satu tahap, bukan harus selesai dengan mengorbankan verifikasi. Jika tahap belum selesai, tandai `in_progress` dan lanjutkan tahap yang sama pada hari berikutnya.
- Jangan membuat data, hasil test, screenshot, metrik, atau klaim runtime palsu.
- Jangan mengubah scope, provider, atau arsitektur terkunci tanpa mencatat blocker dan meminta keputusan pengguna.
- Jangan mengeksekusi deployment produksi, membeli layanan, membuat akun, atau mengubah DNS.
- Commit hanya file yang berkaitan dengan tahap aktif. Jangan memasukkan `.env`, token, CV pribadi, database dump, log sensitif, atau artifact build.
- Commit lokal diperbolehkan setelah quality gates tahap aktif lulus. **Push hanya dilakukan jika perintah harian pengguna secara eksplisit memerintahkan push.**
- Setelah laporan dikirim, berhenti dan tunggu instruksi hari berikutnya.

### File Checkpoint Wajib

Pada Tahap 0, buat `docs/EXECUTION_STATUS.md`. File ini menjadi sumber kebenaran lintas hari dan minimal berisi:

```markdown
# Execution Status

## Current State
- Current stage: 0
- Status: pending | in_progress | verified | blocked
- Branch: ...
- Last commit: ...
- Updated at: ... UTC

## Stage Checklist
- [ ] Stage 0 — Audit and design
- [ ] Stage 1 — Scaffold and quality gates
- [ ] Stage 2 — Database and session API
- [ ] Stage 3 — CV upload and extraction
- [ ] Stage 4 — Candidate context and interview plan
- [ ] Stage 5 — LangGraph text interview
- [ ] Stage 6 — Evidence-based evaluation
- [ ] Stage 7 — Final report
- [ ] Stage 8 — Frontend MVP
- [ ] Stage 9 — Observability, security, reliability
- [ ] Stage 10 — Voice
- [ ] Stage 11 — Optional avatar
- [ ] Stage 12 — Final verification and deployment

## Last Verified Commands
- Command: ...
- Result: ...

## Open Blockers
- None | ...

## Next Allowed Action
- ...
```

Hermes memperbarui file ini pada akhir setiap eksekusi. Tahap hanya boleh ditandai `verified` jika seluruh acceptance criteria tahap tersebut mempunyai bukti.

### Prompt Kontrol Harian

Gunakan template berikut setiap hari:

```text
Lanjutkan project AI Interviewer pada repository dan working directory yang sudah ditentukan.

Hari ini kerjakan hanya Stage <NAMA/NOMOR TAHAP> dari `docs/AI_INTERVIEWER_STEP_BY_STEP_PROMPTS.md`.

Sebelum bekerja:
1. Pastikan repository, working directory, remote, dan branch benar.
2. Baca seluruh aturan repository serta dokumen desain yang relevan.
3. Baca `docs/EXECUTION_STATUS.md` dan verifikasi tahap sebelumnya sudah selesai.
4. Periksa working tree. Jangan menimpa perubahan yang bukan milikmu.

Selama bekerja:
- ikuti scope dan acceptance criteria Stage tersebut;
- jangan lanjut ke Stage berikutnya;
- jangan membuka, menampilkan, atau mengirim secret;
- gunakan OpenCodeProvider dan stub sesuai arsitektur yang dikunci;
- lakukan implementasi, test, dan dokumentasi yang termasuk dalam Stage ini.

Setelah bekerja:
1. Jalankan quality gates yang diwajibkan Stage ini.
2. Perbarui `docs/EXECUTION_STATUS.md` secara jujur.
3. Jika seluruh acceptance criteria verified, buat satu commit lokal dengan pesan `feat(stage-N): <ringkasan>`.
4. <PUSH / JANGAN PUSH>. Jangan push jika instruksi ini masih berupa placeholder.
5. Kirim laporan WhatsApp singkat dengan format:
   - Status
   - Branch dan commit
   - File utama yang berubah
   - Command yang benar-benar dijalankan beserta hasilnya
   - Acceptance criteria yang belum verified
   - Blocker
   - Tahap berikutnya, tetapi jangan mengerjakannya

Jika terhalang credential, layanan eksternal, keputusan arsitektur, atau kegagalan berulang, jangan mengarang solusi atau hasil. Catat blocker, jangan tandai Stage selesai, lalu berhenti.
```

Ganti `<NAMA/NOMOR TAHAP>` dan pilih secara eksplisit `PUSH` atau `JANGAN PUSH` sebelum mengirim prompt kepada Hermes.

## Target Produk

Membangun aplikasi latihan interview berbasis AI yang:

- menerima CV dan job description;
- membuat pertanyaan relevan;
- menjalankan interview teks terlebih dahulu;
- mengajukan follow-up berdasarkan jawaban;
- menilai jawaban dengan bukti berupa kutipan jawaban kandidat;
- menyimpan sesi dan menampilkan laporan;
- dapat dikembangkan menjadi voice interview real-time dan avatar.

## Stack yang Dikunci

- Frontend: Next.js App Router, TypeScript, Tailwind CSS
- Backend: Python 3.12, FastAPI, Pydantic
- Agent workflow: LangGraph
- Database: PostgreSQL
- ORM/migration: SQLAlchemy 2 + Alembic
- Development infrastructure: Docker Compose untuk PostgreSQL
- Testing backend: pytest
- Testing frontend: Vitest dan Testing Library
- Lint/format backend: Ruff
- LLM gateway: OpenCode HTTP server (`opencode serve`), lokal terlebih dahulu
- Observability AI: Langfuse, tetapi baru dipasang setelah alur utama stabil

Model AI harus dibungkus melalui provider interface. Implementasi utama memakai adapter khusus OpenCode HTTP API, bukan menganggap OpenCode sebagai endpoint OpenAI `/v1/chat/completions`. Jangan menyebarkan pemanggilan API OpenCode langsung ke berbagai file. Sediakan `stub` provider agar development dan test tidak membutuhkan OpenCode atau API key.

Konfigurasi awal:

- `OPENCODE_BASE_URL=http://127.0.0.1:4096`
- `OPENCODE_MODEL=<provider/model yang dipilih di OpenCode>`
- `OPENCODE_SERVER_USERNAME` dan `OPENCODE_SERVER_PASSWORD` hanya diperlukan ketika server memakai autentikasi
- URL dan credential hanya dibaca dari environment variable
- aplikasi tidak boleh menganggap OpenCode berarti inference offline; OpenCode dapat meneruskan request ke provider online yang dikonfigurasi
- semua session OpenCode milik aplikasi harus menonaktifkan tools, meminta JSON terstruktur, mempunyai timeout, dan dibersihkan setelah tidak diperlukan

## Aturan Global untuk AI Executor

Tambahkan teks berikut pada bagian akhir **setiap prompt tahap**:

```text
Aturan pengerjaan:
- Periksa repository dan AGENTS.md sebelum mengubah file.
- Jangan menghapus atau menimpa pekerjaan yang tidak berkaitan.
- Jangan memperluas scope di luar tahap ini.
- Jangan meminta atau menuliskan secret. Gunakan hanya nama environment variable dan `.env.example`.
- Pisahkan fakta yang sudah diuji dari asumsi atau pekerjaan yang belum dibuat.
- Gunakan data stub/deterministik untuk automated test; jangan membuat test bergantung pada API AI berbayar.
- Setelah implementasi, jalankan pemeriksaan paling relevan untuk tahap ini.
- Laporkan: file yang berubah, keputusan penting, command yang benar-benar dijalankan, hasil command, dan pekerjaan yang belum selesai.
- Jangan mengatakan selesai apabila acceptance criteria atau test belum terpenuhi.
- Jika menemukan konflik arsitektur yang membutuhkan perubahan besar, berhenti dan jelaskan sebelum mengubahnya.
```

---

## Tahap 0 — Audit dan Rancangan Awal

### Prompt 0

```text
Kamu adalah software architect untuk project portfolio bernama AI Interviewer.

Tujuan produk:
- pengguna mengunggah CV PDF;
- pengguna memasukkan job description dan target role;
- sistem membuat interview adaptif;
- MVP dijalankan melalui teks, bukan voice atau avatar;
- setiap jawaban dinilai menggunakan rubric terstruktur;
- laporan harus menyertakan skor, alasan, dan kutipan jawaban sebagai evidence;
- sesi dan hasil dapat dibuka kembali.

Stack yang dikunci:
- Next.js App Router + TypeScript + Tailwind
- FastAPI + Python 3.12 + Pydantic
- LangGraph
- OpenCode HTTP server sebagai gateway LLM, dengan stub provider untuk test
- PostgreSQL + SQLAlchemy 2 + Alembic
- Docker Compose
- pytest, Ruff, Vitest, Testing Library

Tugasmu pada tahap ini hanya audit dan desain, jangan menulis implementasi fitur.

1. Periksa isi repository, struktur folder, package manager, konfigurasi, dan aturan AGENTS.md.
2. Tentukan apakah project harus dibuat di repository/folder baru atau dapat memakai project yang ada. Jangan mencampurkannya dengan aplikasi yang tidak relevan.
3. Buat dokumen `docs/PRD.md` yang berisi:
   - masalah pengguna;
   - persona;
   - user journey;
   - scope MVP;
   - non-goals: voice, avatar, live coding, admin panel, dan production billing;
   - functional requirements;
   - failure states;
   - acceptance criteria terukur.
4. Buat `docs/ARCHITECTURE.md` yang berisi:
   - batas tanggung jawab frontend, backend, agent, database, dan provider AI;
   - alur data dari upload CV sampai laporan akhir;
   - diagram Mermaid;
   - strategi stub provider;
   - strategi error handling dan idempotency sederhana.
5. Dokumentasikan dua mode runtime LLM: OpenCode lokal pada loopback dan OpenCode cloud yang terautentikasi. Jelaskan bahwa perpindahan dilakukan melalui konfigurasi, bukan perubahan business logic.
6. Buat `docs/DATA_MODEL.md` untuk entitas minimum:
   - InterviewSession
   - SourceDocument
   - InterviewQuestion
   - CandidateAnswer
   - AnswerEvaluation
   - FinalReport
7. Buat `docs/API_CONTRACT.md` dengan endpoint, request, response, validation error, dan status code.
8. Buat `docs/IMPLEMENTATION_PLAN.md` berupa checklist berurutan yang mengikuti tahap-tahap dokumen ini.

Jangan membuat aplikasi, dependency, migration, endpoint, atau UI pada tahap ini.

Acceptance criteria:
- empat dokumen desain tersedia dan konsisten;
- setiap requirement MVP dapat dipetakan ke endpoint serta entitas data;
- non-goals dinyatakan eksplisit;
- tidak ada klaim bahwa fitur sudah bekerja.
```

**Berhenti dan review desainnya sebelum Tahap 1.**

---

## Tahap 1 — Scaffold dan Quality Gates

### Prompt 1

```text
Implementasikan hanya fondasi project berdasarkan dokumen di folder `docs` yang sudah disetujui.

Target struktur minimum:
- `apps/web`: Next.js TypeScript
- `apps/api`: FastAPI Python
- `packages/contracts` atau mekanisme kontrak bersama yang sederhana
- `infra/docker-compose.yml`: PostgreSQL lokal

Tugas:
1. Scaffold frontend dan backend tanpa fitur bisnis.
2. Tambahkan endpoint backend `GET /health` dengan response terstruktur.
3. Tambahkan halaman frontend sederhana yang memeriksa health backend dan menampilkan status loading, connected, atau error.
4. Tambahkan `.env.example`; pastikan file secret lokal di-ignore.
5. Siapkan command development, lint, type-check, test, dan build.
6. Tambahkan README berisi command PowerShell yang benar dan lokasi runtime masing-masing.
7. Tambahkan minimal satu test backend untuk health endpoint dan satu test frontend untuk representasi status health.

Jangan membuat autentikasi, upload CV, LangGraph, interview, voice, avatar, atau dashboard.

Acceptance criteria:
- backend dapat start dan `/health` mengembalikan 200;
- frontend dapat start dan membaca health backend;
- lint, type-check, test, dan production build lulus;
- PostgreSQL container dapat start dan health check-nya sehat.
```

---

## Tahap 2 — Database dan Session API

### Prompt 2

```text
Implementasikan persistence dan lifecycle dasar interview session sesuai `docs/DATA_MODEL.md` dan `docs/API_CONTRACT.md`.

Tugas:
1. Konfigurasikan SQLAlchemy async dan Alembic.
2. Implementasikan tabel minimum untuk session, source document, question, answer, evaluation, dan final report.
3. Gunakan UUID, timestamp UTC, foreign key, constraint, serta enum/status yang jelas.
4. Buat repository/service layer agar route tidak berisi query database langsung.
5. Implementasikan endpoint minimum:
   - membuat draft session;
   - mengambil detail session;
   - menampilkan daftar session terbaru;
   - menghapus draft yang belum dimulai, jika operasi ini memang ada di kontrak.
6. Tambahkan migration pertama dan seed hanya jika benar-benar dibutuhkan.
7. Tambahkan integration test database dengan database test yang terisolasi.

Jangan menambahkan AI, upload file, LangGraph, scoring, voice, atau avatar.

Acceptance criteria:
- migration dapat dijalankan pada database kosong;
- CRUD session minimum bekerja melalui API;
- status transition yang tidak valid ditolak;
- test membuktikan data tersimpan dan dapat dibaca kembali;
- OpenAPI sesuai kontrak yang disepakati.
```

---

## Tahap 3 — Upload dan Ekstraksi CV

### Prompt 3

```text
Implementasikan upload CV PDF dan ekstraksi teks yang aman untuk MVP.

Scope:
- hanya PDF;
- satu CV per interview session;
- batasi ukuran file dan jumlah halaman;
- gunakan text extraction untuk PDF yang memang memiliki text layer;
- OCR belum termasuk tahap ini.

Tugas:
1. Buat validasi MIME, ekstensi, ukuran, signature file, dan page count.
2. Jangan mempercayai nama file dari pengguna untuk path penyimpanan.
3. Ekstrak teks per halaman dan simpan metadata halaman agar evidence dapat ditelusuri.
4. Simpan hanya data yang diperlukan sesuai keputusan desain.
5. Tandai dokumen dengan status `uploaded`, `processing`, `ready`, atau `failed`.
6. Tambahkan endpoint upload dan endpoint status dokumen.
7. Pastikan error parsing tidak membuat session rusak.
8. Buat fixture PDF kecil untuk automated test.

Jangan menambahkan OCR, embeddings, RAG, interview agent, voice, atau avatar.

Acceptance criteria:
- PDF valid menghasilkan teks per halaman;
- file palsu, terlalu besar, terenkripsi, kosong, dan rusak ditolak dengan pesan aman;
- test tidak memakai file atau layanan eksternal;
- tidak ada path traversal dan file sementara dibersihkan.
```

---

## Tahap 4 — Konteks Kandidat dan Interview Plan

### Prompt 4

```text
Implementasikan pembuatan konteks kandidat dan interview plan menggunakan provider AI yang dapat diganti.

Input:
- teks CV hasil ekstraksi;
- target role;
- job description;
- preferensi bahasa interview.

Output terstruktur:
- ringkasan profil kandidat;
- skills yang benar-benar ditemukan dalam CV;
- requirement penting dari job description;
- area yang cocok dan gap yang perlu digali;
- interview plan berisi 5 pertanyaan awal dengan competency, objective, difficulty, dan expected evidence.

Tugas:
1. Definisikan interface `LLMProvider`.
2. Buat `StubLLMProvider` deterministik untuk test/local development.
3. Buat `OpenCodeProvider` yang menggunakan API resmi dari `opencode serve`. Gunakan `OPENCODE_BASE_URL`, model, username, dan password dari environment variable. Jangan mengasumsikan endpoint OpenAI-compatible.
4. Gunakan Pydantic schema untuk structured output; validasi seluruh respons model.
5. Jangan membiarkan model mengarang skill kandidat yang tidak ada di CV.
6. Simpan interview plan ke database.
7. Tambahkan endpoint generate plan yang idempotent atau memiliki aturan regenerate yang eksplisit.
8. Tambahkan unit dan integration test menggunakan stub.
9. Untuk request OpenCode: buat session aplikasi yang terisolasi, matikan seluruh tools, minta JSON saja, terapkan timeout, dan hapus session sementara setelah hasil selesai diproses.
10. Tambahkan health/readiness check yang membedakan backend aplikasi hidup dengan OpenCode tersedia.

Jangan membuat loop interview, scoring, voice, avatar, atau RAG perusahaan.

Acceptance criteria:
- output invalid dari provider ditolak atau di-retry secara terbatas;
- seluruh pertanyaan mempunyai competency dan objective;
- test membuktikan plan tersimpan;
- aplikasi tetap dapat didemokan penuh dalam stub mode tanpa API key.
- perpindahan OpenCode lokal ke cloud hanya memerlukan perubahan environment variable;
- test membuktikan tools tidak diberikan kepada session interviewer.
```

---

## Tahap 5 — LangGraph Interview Teks

### Prompt 5

```text
Implementasikan workflow interview teks menggunakan LangGraph.

State minimum:
- session_id;
- interview status;
- interview plan;
- current question index;
- current question;
- question history;
- answer history;
- follow-up count per question;
- remaining question count;
- completion reason.

Node minimum:
- load_session;
- select_question;
- wait_for_answer atau human-input boundary;
- classify_answer;
- decide_follow_up;
- persist_turn;
- advance_or_finish.

Aturan:
- maksimal 5 pertanyaan utama;
- maksimal 1 follow-up untuk setiap pertanyaan utama;
- follow-up hanya muncul jika jawaban terlalu umum, tidak relevan, atau butuh evidence;
- jangan menilai final di node interviewer;
- state penting harus dapat dipulihkan setelah restart;
- ulang request yang sama tidak boleh menggandakan jawaban atau pertanyaan.

Implementasikan endpoint:
- start interview;
- mendapatkan pertanyaan aktif;
- mengirim jawaban teks;
- melanjutkan ke pertanyaan berikutnya;
- mengakhiri interview.

Tambahkan test graph untuk jalur:
- jawaban cukup → pertanyaan berikutnya;
- jawaban kurang jelas → follow-up;
- batas follow-up tercapai;
- seluruh pertanyaan selesai;
- session direstart lalu dilanjutkan;
- duplicate submission tidak menggandakan turn.

Jangan menambahkan voice, avatar, atau UI dashboard kompleks.

Acceptance criteria:
- workflow deterministik di stub mode;
- state dapat dipulihkan;
- semua transition memiliki test;
- jumlah pertanyaan dan follow-up tidak melewati batas.
```

---

## Tahap 6 — Evaluation Engine Berbasis Evidence

### Prompt 6

```text
Implementasikan evaluation engine terpisah dari interviewer.

Rubric per jawaban:
- relevance: 0–5;
- technical_accuracy: 0–5;
- clarity: 0–5;
- evidence_specificity: 0–5;
- structure: 0–5;
- overall: dihitung oleh kode dari bobot yang terdokumentasi, bukan dipercaya langsung dari model.

Setiap evaluasi wajib memiliki:
- score per dimensi;
- short rationale;
- evidence quote yang berasal persis dari jawaban kandidat;
- strengths;
- improvements;
- confidence;
- status `evaluated`, `needs_review`, atau `insufficient_answer`.

Tugas:
1. Buat schema evaluation yang ketat.
2. Validasi bahwa setiap evidence quote benar-benar substring dari jawaban kandidat.
3. Bila evidence tidak valid, jangan simpan sebagai evaluasi sukses.
4. Hitung overall score melalui kode deterministik.
5. Bedakan jawaban lemah dengan kegagalan provider.
6. Simpan evaluation dan versi rubric/prompt.
7. Buat endpoint untuk evaluasi satu jawaban dan mengambil hasilnya.
8. Tambahkan test untuk skor batas, quote palsu, output model rusak, jawaban kosong, retry, serta persistence.

Jangan membuat final report, voice, avatar, atau klaim bahwa skor AI adalah penilaian rekrutmen objektif.

Acceptance criteria:
- skor selalu berada pada rentang yang benar;
- evidence quote tervalidasi;
- overall konsisten dengan formula;
- kegagalan provider tidak disimpan sebagai skor nol kandidat;
- seluruh test menggunakan stub provider.
```

---

## Tahap 7 — Final Report

### Prompt 7

```text
Implementasikan final report setelah interview selesai.

Isi laporan:
- ringkasan interview;
- skor per competency;
- overall score dengan formula transparan;
- strengths berdasarkan evaluation yang tersimpan;
- top 3 improvements;
- contoh jawaban kandidat yang mendukung kesimpulan;
- rekomendasi latihan;
- daftar pertanyaan dan evaluasi per jawaban;
- disclaimer bahwa laporan adalah alat latihan, bukan keputusan hiring.

Aturan:
- agregasi numerik dilakukan oleh kode;
- model hanya boleh merangkum data evaluasi yang sudah tervalidasi;
- jangan membuat evidence baru;
- jika evaluasi belum lengkap, report berstatus `incomplete` dan menjelaskan bagian yang hilang;
- generate ulang tidak boleh membuat duplikasi report tanpa versioning yang jelas.

Tugas:
1. Implementasikan service dan endpoint generate/get report.
2. Simpan input provenance: question ID, answer ID, dan evaluation ID.
3. Tambahkan export JSON. PDF belum termasuk MVP kecuali sudah disetujui di PRD.
4. Tambahkan test agregasi, missing evaluation, evidence provenance, dan idempotency.

Acceptance criteria:
- angka report dapat ditelusuri ke evaluation;
- kutipan dapat ditelusuri ke answer;
- report incomplete tidak dipresentasikan sebagai final;
- test membuktikan report dapat dibuka kembali setelah restart.
```

---

## Tahap 8 — Frontend MVP Lengkap

### Prompt 8

```text
Bangun frontend MVP berdasarkan API yang sudah diuji. Jangan memindahkan business logic backend ke frontend.

Halaman minimum:
1. Home / daftar sesi.
2. Setup interview:
   - upload CV;
   - target role;
   - job description;
   - bahasa;
   - generate interview plan.
3. Interview room teks:
   - satu pertanyaan aktif;
   - textarea jawaban;
   - submit state;
   - indikator progress;
   - tampilan follow-up yang jelas;
   - tombol end dengan konfirmasi.
4. Result page:
   - overall dan dimension scores;
   - evidence quote;
   - strengths;
   - improvements;
   - rekomendasi latihan;
   - daftar evaluasi setiap jawaban.

Tugas:
- buat API client bertipe;
- tangani loading, empty, error, retry, dan disabled state;
- cegah double submission;
- buat UI responsive dan keyboard accessible;
- jangan menyimpan CV atau API key di localStorage;
- tambahkan component test untuk form, turn submission, error state, dan result rendering;
- tambahkan minimal satu end-to-end happy path memakai backend stub mode jika tooling project memungkinkan.

Jangan menambahkan voice, avatar, authentication, payment, atau admin panel.

Acceptance criteria:
- pengguna dapat menyelesaikan alur setup → interview → report;
- refresh halaman tidak kehilangan session aktif;
- double click tidak menggandakan jawaban;
- tidak ada skor/evidence dummy pada runtime normal;
- lint, type-check, test, dan production build lulus.
```

---

## Tahap 9 — Observability, Security, dan Reliability

### Prompt 9

```text
Perkuat MVP yang sudah bekerja tanpa menambah fitur produk baru.

Tugas observability:
- tambahkan correlation ID dan structured logging;
- trace workflow LangGraph dan pemanggilan provider;
- integrasikan Langfuse melalui environment variable opsional;
- jangan mencatat CV lengkap, job description lengkap, jawaban lengkap, token, atau secret secara default;
- catat latency, provider, model, token usage jika tersedia, status, dan error category.

Tugas security/reliability:
- audit upload handling;
- tambahkan request size limit;
- rate limit endpoint AI yang mahal;
- timeout dan retry terbatas;
- sanitasi error untuk client;
- CORS hanya untuk origin yang dikonfigurasi;
- validasi session ownership boundary meskipun MVP masih anonymous;
- dependency audit;
- concurrency dan duplicate-request test;
- privacy retention policy di dokumentasi.
- lindungi OpenCode cloud dengan autentikasi dan TLS; jangan mengekspos server tanpa password langsung ke internet;
- jangan meneruskan endpoint OpenCode atau credential ke browser.

Tambahkan dokumentasi threat model sederhana dan runbook kegagalan provider.

Acceptance criteria:
- aplikasi tetap berjalan tanpa Langfuse;
- trace berhasil dikirim hanya ketika konfigurasi tersedia;
- secret dan isi sensitif tidak muncul di log test;
- timeout/retry/rate-limit memiliki test;
- semua quality gates lama tetap lulus.
```

---

## Tahap 10 — Voice Tanpa Avatar

### Prompt 10

```text
Tambahkan mode voice sebagai lapisan input/output di atas workflow interview yang sudah stabil. Mode teks harus tetap tersedia sebagai fallback.

Sebelum implementasi, buat decision record yang membandingkan:
- browser MediaRecorder + request/response audio;
- streaming WebSocket/WebRTC;
- provider STT/TTS yang dipilih;
- biaya, latency, dukungan Bahasa Indonesia, dan kompleksitas.

Untuk versi pertama, prioritaskan solusi paling sederhana yang tetap dapat diuji.

Tugas:
- rekam audio dengan izin eksplisit;
- tampilkan state `requesting permission`, `listening`, `processing`, `speaking`, dan `error`;
- transkripsikan audio menjadi teks;
- tampilkan dan izinkan pengguna mengoreksi transcript sebelum submit;
- ubah pertanyaan AI menjadi audio;
- sediakan stop playback dan kembali ke mode teks;
- jangan menyimpan audio secara permanen tanpa persetujuan eksplisit;
- abstraksikan STT dan TTS melalui provider interface;
- sediakan stub provider dan fixture audio untuk test.

Jangan menambahkan avatar pada tahap ini.

Acceptance criteria:
- pengguna dapat menyelesaikan interview dengan voice atau teks;
- penolakan izin mikrofon tidak memblokir mode teks;
- transcript selalu terlihat sebelum menjadi jawaban final;
- error STT/TTS tidak merusak state interview;
- automated test tidak membutuhkan akun provider berbayar.
```

---

## Tahap 11 — Avatar Opsional

### Prompt 11

```text
Tambahkan avatar hanya sebagai presentation layer opsional setelah voice interview terbukti stabil.

Sebelum coding:
1. Audit dokumentasi provider avatar terkini.
2. Catat pricing, free-tier limit, data retention, biometric/privacy implications, browser support, dan fallback behavior.
3. Buat architecture decision record dan tunggu persetujuan sebelum memasang SDK.

Setelah disetujui:
- integrasikan avatar melalui adapter agar provider dapat diganti;
- sinkronkan audio TTS dengan avatar;
- sediakan toggle avatar on/off;
- tampilkan fallback statis ketika avatar gagal;
- jangan biarkan kegagalan avatar menghentikan interview;
- jangan mengirim video kandidat ke provider avatar kecuali benar-benar diperlukan dan disetujui;
- ukur latency dan kegagalan, bukan membuat klaim performa tanpa pengujian.

Acceptance criteria:
- mode text dan voice tetap bekerja tanpa avatar;
- kegagalan avatar terisolasi;
- consent dan privacy notice terlihat;
- biaya dan batas provider terdokumentasi dari sumber resmi terkini;
- integrasi diuji minimal melalui sandbox/provider test yang sah.
```

---

## Tahap 12 — Final Verification dan Deployment

### Prompt 12

```text
Lakukan audit kesiapan deployment terhadap seluruh AI Interviewer. Jangan menambah fitur baru.

Tugas:
1. Cocokkan implementasi dengan PRD dan tandai setiap acceptance criterion sebagai verified, failed, atau not tested.
2. Jalankan dari database kosong:
   - install;
   - migration;
   - backend lint/test;
   - frontend lint/type-check/test/build;
   - integration test;
   - end-to-end happy path dalam stub mode.
3. Uji manual satu alur provider nyata hanya jika key sudah tersedia secara lokal; jangan meminta key ditampilkan.
4. Verifikasi upload error, provider timeout, refresh saat interview, duplicate submit, incomplete report, dan database restart.
5. Audit `.gitignore`, git tracked files, log, dan build artifact untuk memastikan tidak ada secret atau CV pengguna.
6. Buat:
   - `docs/DEPLOYMENT.md`;
   - `docs/RUNBOOK.md`;
   - `docs/VERIFICATION_REPORT.md`;
   - `.env.example` final.
7. Dokumentasikan environment frontend, backend, database, storage, CORS, migration command, health check, rollback, dan backup.

Jangan menyatakan production-ready hanya karena build lulus.

Acceptance criteria:
- verification report menyertakan command dan output ringkas yang benar-benar dijalankan;
- semua blocker diberi status yang jujur;
- deployment dapat direproduksi dari dokumentasi;
- secret scan tidak menemukan credential;
- aplikasi berhasil menjalankan alur setup → interview → evaluation → report pada environment deployment atau staging.
```

---

## Prompt Perbaikan Jika AI Mengaku Selesai Tanpa Bukti

```text
Jangan lanjut membuat fitur baru. Audit ulang klaim penyelesaian tahap terakhir.

1. Tampilkan acceptance criteria tahap tersebut satu per satu.
2. Untuk setiap item, berikan status: verified, failed, atau not tested.
3. Sertakan file yang menjadi bukti dan command yang benar-benar dijalankan.
4. Jalankan ulang test paling sempit yang relevan.
5. Jika gagal, perbaiki hanya penyebab kegagalan tersebut lalu jalankan ulang.
6. Jangan menyamakan type-check, unit test, build, dan runtime test; laporkan masing-masing secara terpisah.
7. Jangan mengatakan selesai selama masih ada acceptance criterion yang failed atau not tested.
```

## Urutan Pemakaian

```text
Prompt 0 → review dan setujui desain
Prompt 1 → scaffold
Prompt 2 → database
Prompt 3 → CV processing
Prompt 4 → interview plan
Prompt 5 → interview workflow
Prompt 6 → evaluation
Prompt 7 → report
Prompt 8 → frontend lengkap
Prompt 9 → reliability
Prompt 10 → voice
Prompt 11 → avatar opsional
Prompt 12 → deployment verification
```

MVP portfolio sudah dapat dianggap terbentuk setelah **Tahap 9**. Voice dan avatar adalah pengembangan lanjutan, bukan syarat agar inti project bernilai.
