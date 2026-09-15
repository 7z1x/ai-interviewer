# AI System — AI Interviewer

> Kontrak desain untuk perilaku AI. Belum ada klaim bahwa integrasi atau kualitas model telah terverifikasi pada runtime.

## 1. Batas Tanggung Jawab

Model membantu menghasilkan interview plan, mengklasifikasikan kecukupan jawaban, menyusun follow-up, dan mengusulkan evaluasi terstruktur. Kode aplikasi tetap bertanggung jawab atas validasi, status transition, batas pertanyaan, idempotency, perhitungan skor, authorization, dan persistence.

Model tidak boleh menjadi sumber kebenaran untuk identitas, izin akses, numeric aggregate, evidence validity, atau keberhasilan operasi database.

## 2. Provider Boundary

Semua pemanggilan model melewati satu interface `LLMProvider`. Implementasi minimum:

- `StubLLMProvider`: deterministik, tanpa network atau API key, untuk automated test dan demo lokal.
- `OpenCodeProvider`: adapter tunggal untuk HTTP API resmi `opencode serve`; tidak mengasumsikan endpoint OpenAI-compatible.

Business logic tidak boleh mengetahui URL, authentication detail, atau format transport provider. Perpindahan provider hanya melalui dependency injection dan environment configuration.

Detail endpoint OpenCode wajib diverifikasi kembali terhadap dokumentasi/instance yang digunakan pada Stage 4. Contoh endpoint dalam dokumen desain bukan bukti kompatibilitas runtime.

## 3. Provider Operations

Interface harus memisahkan operasi berikut agar setiap output mempunyai schema dan test sendiri:

- `generate_interview_plan`
- `classify_answer`
- `generate_follow_up`
- `evaluate_answer`
- `summarize_final_report`

Setiap operasi mempunyai timeout eksplisit, error category, correlation ID, prompt version, model identifier, dan schema version.

## 4. Structured Output

- Seluruh output provider diperlakukan sebagai untrusted input.
- Output harus berbentuk JSON dan divalidasi menggunakan Pydantic sebelum digunakan.
- Unknown field ditolak untuk kontrak kritis agar perubahan provider tidak masuk diam-diam.
- Range, panjang string, jumlah item, enum, dan field wajib divalidasi.
- Parsing atau validation failure boleh di-retry secara terbatas jika kegagalannya transient atau format-related.
- Setelah retry habis, operasi gagal secara eksplisit dan tidak menyimpan resource seolah-olah sukses.

## 5. Grounding Rules

### Interview plan

- Skill kandidat hanya boleh dimasukkan jika memiliki evidence dari CV yang telah diekstrak.
- Requirement lowongan harus dapat ditelusuri ke job description yang diberikan.
- Ketidakcocokan atau informasi yang tidak tersedia ditandai sebagai gap/unknown, bukan dilengkapi oleh model.

### Answer evaluation

- `evidence_quote` harus merupakan kutipan literal dari jawaban kandidat setelah normalisasi minimal yang terdokumentasi.
- Validasi kecocokan quote dilakukan oleh kode, bukan model.
- Quote tidak valid menyebabkan evaluasi ditolak atau berstatus `needs_review`.
- Jawaban kosong/terlalu pendek dibedakan dari provider failure.

### Final report

- Semua angka dihitung oleh kode dari evaluasi tervalidasi.
- Model hanya boleh merangkum data yang telah tervalidasi.
- Report menyimpan provenance ke question, answer, dan evaluation ID.

## 6. Interview and Evaluation Separation

Interviewer menentukan pertanyaan berikutnya dan follow-up, tetapi tidak menentukan final score. Evaluator bekerja dari pertanyaan, objective, rubric, dan jawaban tersimpan. Pemisahan ini mencegah keputusan alur percakapan mengubah rumus penilaian secara tersembunyi.

Batas workflow ditegakkan oleh kode:

- tepat maksimal lima pertanyaan utama;
- maksimal satu follow-up per pertanyaan utama;
- duplicate submission tidak menambah turn;
- state dapat dipulihkan dari database.

## 7. Scoring Contract

Dimensi per jawaban berada pada rentang 0–5:

- relevance;
- technical accuracy;
- clarity;
- evidence specificity;
- structure.

Bobot dan rumus `overall` harus menjadi fungsi kode yang diuji. Model tidak boleh mengirim nilai aggregate yang langsung dipercaya. Perubahan rubric atau bobot memerlukan versi baru dan evaluation regression.

## 8. Prompt and Model Versioning

- Prompt disimpan sebagai template/versioned module, bukan string tersebar di route.
- Hasil AI menyimpan `provider`, `model`, `prompt_version`, `schema_version`, dan `rubric_version` yang relevan.
- Perubahan prompt, model, parameter, schema, atau rubric harus dicatat dan menjalankan evaluation suite.
- Jangan mengklaim versi baru lebih baik hanya dari beberapa contoh manual.

## 9. Timeout, Retry, and Failure

- Timeout ditentukan per operation dan dapat dikonfigurasi dengan batas aman.
- Retry maksimal 1–2 kali dengan backoff untuk timeout, rate limit, atau malformed output yang masuk kategori retryable.
- Jangan retry validation failure yang deterministik tanpa mengubah strategi request.
- Session sementara OpenCode harus dibersihkan pada success maupun failure.
- Provider unavailable tidak boleh membuat liveness backend gagal; expose readiness terpisah.
- Provider failure tidak pernah dikonversi menjadi skor nol kandidat.

Nilai timeout final ditetapkan setelah pengukuran runtime; angka contoh di dokumen bukan konfigurasi produksi.

## 10. OpenCode Session Rules

- Base URL dan credential hanya berasal dari environment variable backend.
- Session aplikasi terisolasi untuk setiap operation atau lifecycle yang disepakati.
- Tools dimatikan secara eksplisit.
- Provider hanya diminta menghasilkan structured data sesuai schema.
- URL dan credential tidak pernah diteruskan ke browser.
- Mode cloud wajib memakai TLS dan authentication.
- OpenCode adalah gateway dan dapat meneruskan request ke provider online; jangan menyebutnya inference offline tanpa bukti konfigurasi.

## 11. Evaluation Strategy

Sebelum klaim kualitas dibuat, siapkan versioned evaluation dataset yang mencakup:

- CV tipis, sedang, dan kompleks;
- job description Indonesia dan Inggris;
- skill eksplisit dan skill yang tidak terdapat di CV;
- jawaban relevan, vague, tidak relevan, kosong, dan adversarial;
- evidence quote valid dan palsu;
- output provider malformed dan out-of-range.

Metric minimum:

- schema validity rate;
- unsupported-skill rate;
- evidence-quote validity rate;
- follow-up decision agreement terhadap label manusia;
- score agreement/tolerance terhadap rubric reference;
- end-to-end success rate;
- p50/p95 latency;
- token/cost per completed session jika provider menyediakan data tersebut.

Threshold kelulusan belum ditetapkan. Tetapkan setelah baseline dataset dibuat; jangan membuat angka target tanpa evidence awal.

## 12. Observability and Privacy

Log/trace boleh menyimpan operation name, status, latency, token count, error category, serta versi model/prompt/schema. CV, job description, jawaban lengkap, evidence lengkap, credential, dan raw provider response tidak boleh masuk log default.

Langfuse bersifat opsional. Aplikasi harus tetap berjalan tanpa Langfuse, dan keberhasilan mengirim trace bukan bukti bahwa isi trace benar sampai diverifikasi melalui read-back yang tersedia.
