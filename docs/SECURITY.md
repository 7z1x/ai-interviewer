# Security and Privacy — AI Interviewer

> Baseline desain keamanan MVP. Kontrol harus diverifikasi saat implementasi; keberadaan dokumen ini bukan bukti keamanan runtime.

## 1. Data Classification

| Data | Klasifikasi | Aturan utama |
|---|---|---|
| CV dan extracted text | sensitif/personal | jangan log; akses hanya oleh owner session; retensi terbatas |
| Job description | internal user input | jangan log isi lengkap secara default |
| Jawaban dan evidence quote | sensitif/personal | jangan log isi lengkap; ikut retensi session |
| Report dan score | sensitif | akses hanya oleh owner session |
| API key/credential | secret | backend environment/secret store saja; tidak ke browser/database/log |
| Metadata teknis | operasional | boleh dilog jika tidak memuat isi personal |

## 2. Anonymous Session Ownership

MVP tidak memakai akun, tetapi setiap session tetap wajib mempunyai ownership boundary. Gunakan random opaque owner token dengan entropy memadai, simpan hash token di backend, kirim token melalui cookie `HttpOnly`, `Secure` di production, dan `SameSite=Lax` atau lebih ketat sesuai flow.

UUID session bukan credential. Mengetahui session ID tidak boleh cukup untuk membaca, mengubah, atau menghapus session. Detail implementasi final dicatat dalam ADR sebelum Stage 2/9.

## 3. Upload Policy

Baseline MVP dikunci sebagai berikut:

- hanya satu PDF per session;
- maksimum 5 MiB;
- maksimum 10 halaman;
- tidak menerima PDF terenkripsi, rusak, kosong, atau tanpa text layer;
- validasi extension, declared MIME, magic bytes, parser result, size, dan page count;
- gunakan ID acak untuk path internal, bukan nama file user;
- jangan melayani kembali upload melalui path publik;
- proses dengan least privilege dan bersihkan temporary file pada success/failure;
- OCR tidak termasuk MVP.

Perubahan batas harus dilakukan melalui konfigurasi tervalidasi dan disinkronkan ke PRD, API contract, UI copy, serta test.

## 4. Storage and Retention

Keputusan default MVP:

- raw PDF dihapus setelah ekstraksi sukses dan persistensi extracted text terkonfirmasi;
- extracted text, answers, evaluations, dan reports disimpan maksimal 30 hari;
- user dapat menghapus draft/session miliknya sesuai lifecycle yang disepakati;
- cleanup job harus idempotent dan dapat diaudit melalui metadata tanpa mencatat isi data;
- backup/deployment yang belum mempunyai retention policy tidak boleh memakai data CV nyata.

Jika kebutuhan produk mengharuskan raw PDF disimpan, buat ADR baru yang menetapkan alasan, encryption at rest, access control, lokasi storage, dan jadwal penghapusan.

## 5. AI Provider Boundary

- Beritahu user bahwa CV, job description, dan jawaban yang diperlukan dapat diproses oleh provider AI eksternal.
- Kirim data minimum yang diperlukan untuk satu operation.
- Jangan mengirim secret, cookie, internal path, database record lain, atau log.
- Session interviewer harus menonaktifkan tools.
- OpenCode cloud wajib TLS dan authentication; instance tanpa auth yang dapat diakses publik adalah deployment blocker.
- Raw provider request/response tidak dicatat pada production log.

## 6. API Controls

- Runtime validation pada seluruh request.
- Body-size limit global dan limit khusus upload.
- Rate limit lebih ketat pada endpoint yang memanggil AI.
- Idempotency untuk plan, answer, evaluation, dan report sesuai contract.
- CORS allowlist eksplisit; jangan memakai wildcard bersama credential.
- Error response disanitasi dan tidak mengandung stack trace, filesystem path, SQL, atau credential.
- Authentication dan authorization check berada di backend service/boundary.

Nilai rate limit final ditentukan setelah runtime profile tersedia. Jangan mengarang angka produksi sebelum Stage 9.

## 7. Logging and Observability

Log boleh berisi request/correlation ID, route template, status, latency, error category, resource ID, dan versi model/prompt/schema. Log tidak boleh berisi CV, extracted text, job description lengkap, jawaban lengkap, evidence quote lengkap, authorization header, cookie, token, password, atau raw provider payload.

Trace Langfuse mengikuti aturan redaction yang sama dan harus opsional.

## 8. Secret Management

- Semua credential dibaca dari environment variable atau secret store runtime.
- `.env.example` hanya berisi nama variable dan nilai placeholder aman.
- `.env*` lokal harus di-ignore, kecuali `.env.example`.
- Jangan mengirim secret melalui chat, WhatsApp, issue, commit, screenshot, atau test fixture.
- Lakukan secret scan pada CI/final verification.

## 9. Dependency and Deployment

- Gunakan dependency resmi, maintained, dan versi yang kompatibel.
- Audit dependency setelah lockfile tersedia; bedakan vulnerability exploitable dari dependency dev/non-runtime.
- Production menggunakan HTTPS, secure cookie, restricted database/network access, dan non-root container jika memungkinkan.
- Jangan deploy production, membuat akun, membeli layanan, atau mengubah DNS tanpa instruksi eksplisit pengguna.

## 10. Security Verification

Minimal uji:

- akses session tanpa/salah owner token ditolak;
- session ID enumeration tidak memberikan data;
- upload palsu, besar, terenkripsi, rusak, dan path-like filename ditolak;
- duplicate/concurrent request tidak menggandakan resource;
- provider error tidak membocorkan response mentah;
- log dan trace bebas dari data terlarang;
- aplikasi berjalan aman ketika Langfuse atau OpenCode tidak tersedia;
- retention cleanup hanya menghapus target yang memenuhi syarat.
