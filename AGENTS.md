# AI Interviewer — Agent Rules

Aturan ini berlaku untuk seluruh repository. `AGENTS.md` yang lebih dekat dengan file yang dikerjakan boleh menambah aturan khusus, tetapi tidak boleh melemahkan aturan root ini.

## Sources of Truth

Jika dokumen bertentangan, gunakan urutan berikut:

1. `docs/PRD.md` — scope dan perilaku produk.
2. `docs/API_CONTRACT.md` — kontrak HTTP.
3. `docs/DATA_MODEL.md` — schema dan constraint data.
4. `docs/ARCHITECTURE.md` — batas komponen.
5. `docs/AI_SYSTEM.md` — perilaku, validasi, dan evaluasi AI.
6. `docs/SECURITY.md` — kontrol keamanan dan privasi.
7. `docs/TESTING.md` — bukti verifikasi yang diwajibkan.
8. `docs/IMPLEMENTATION_PLAN.md` — urutan implementasi.
9. `docs/EXECUTION_STATUS.md` — checkpoint pekerjaan saat ini.

Jangan mengubah kontrak atau arsitektur diam-diam agar cocok dengan implementasi. Catat keputusan yang sulit dibalik di `docs/decisions/` terlebih dahulu.

## Before Editing

- Jalankan `git status --short --branch` dan periksa branch aktif.
- Baca dokumen yang berkaitan dengan task serta `docs/EXECUTION_STATUS.md`.
- Periksa implementasi dan pola yang sudah ada sebelum membuat file atau abstraction baru.
- Kerjakan hanya stage aktif dan jangan memperluas scope tanpa persetujuan.
- Jangan menghapus atau menimpa perubahan yang tidak dipahami.
- Jangan mulai stage berikutnya sebelum stage aktif berstatus `verified`.

## Code Organization

- Target file handwritten maksimal 300 baris. Melewati batas ini memicu review tanggung jawab, bukan pemecahan file secara paksa.
- Generated files, migration, fixture, snapshot, dan konfigurasi deklaratif dikecualikan dari target 300 baris.
- Satu module mempunyai satu tanggung jawab utama.
- Route/controller hanya menangani HTTP boundary; business logic berada di service/domain layer; query berada di repository/data-access layer.
- Pemanggilan model hanya melalui `LLMProvider`. Jangan menyebarkan request OpenCode ke module lain.
- Hindari fungsi lebih dari 50 baris atau kompleksitas tinggi tanpa alasan yang jelas.
- Jangan membuat abstraction hanya untuk mengantisipasi kebutuhan yang belum ada.

## Types and Validation

- TypeScript memakai strict mode; jangan gunakan `any` tanpa alasan yang dicatat.
- Python memakai type hints pada public interface dan service boundary.
- Type statis tidak menggantikan runtime validation.
- Validasi request, response provider, file, environment variable, dan data eksternal pada boundary.
- Gunakan Pydantic untuk kontrak backend dan structured AI output.
- Jangan menduplikasi enum, status, schema, atau business rule di beberapa layer.

## AI Safety and Reliability

- Perlakukan seluruh output model sebagai untrusted input.
- Semua structured output wajib lolos schema validation sebelum disimpan atau ditampilkan.
- Session OpenCode milik interviewer tidak boleh mempunyai tools.
- Catat versi prompt, model, schema, dan rubric pada output yang relevan.
- Gunakan timeout eksplisit dan retry terbatas hanya untuk transient failure.
- Automated test wajib memakai stub deterministik, bukan API AI berbayar.
- Skill kandidat hanya boleh berasal dari bukti CV yang tersedia.
- Evidence quote wajib cocok secara deterministik dengan jawaban kandidat.
- Provider failure tidak boleh diubah menjadi skor nol kandidat.
- Jangan menyatakan model akurat atau production-ready tanpa evaluation dataset dan hasil yang benar-benar dijalankan.
- Jika grounding atau evidence gagal, fail closed dan tampilkan status yang jujur.

## Security and Privacy

- Jangan membaca, mencetak, menyimpan, atau commit secret.
- Jangan memasukkan CV, job description, jawaban lengkap, credential, atau token ke log/trace.
- Validasi ekstensi, MIME, magic bytes, ukuran, jumlah halaman, enkripsi, dan hasil parsing PDF.
- Jangan gunakan nama file dari user sebagai path penyimpanan.
- Authorization wajib diperiksa backend; menyembunyikan tombol frontend tidak cukup.
- Destructive migration atau penghapusan data material membutuhkan persetujuan pengguna.
- Ikuti keputusan rinci di `docs/SECURITY.md`.

## Verification

Jalankan pemeriksaan yang tersedia dan relevan untuk perubahan:

1. format check;
2. lint;
3. typecheck;
4. unit test;
5. integration atau graph test;
6. production build;
7. runtime check pada route/alur yang diubah;
8. AI evaluation jika prompt, model, schema, atau rubric berubah.

- Jangan mengarang command atau hasil test.
- Jangan mengatakan selesai jika acceptance criteria belum mempunyai bukti.
- Bedakan lint error, type error, test failure, build failure, runtime failure, dan pekerjaan yang belum diuji.
- Build yang lulus tidak membuktikan route atau integrasi eksternal bekerja.

## Git and Status

- Jangan commit atau push kecuali pengguna memintanya.
- Jangan memakai force push, `git reset --hard`, atau menghapus perubahan yang tidak berkaitan.
- Jangan commit `.env`, CV, database dump, log sensitif, atau build artifact.
- Perbarui `docs/EXECUTION_STATUS.md` pada akhir eksekusi, tetapi jangan menulis ulang bukti historis sebagai hasil baru.
- Stage hanya boleh ditandai `verified` jika seluruh acceptance criteria stage tersebut mempunyai bukti.

## Reporting

Laporan akhir harus menyebutkan:

- status pekerjaan;
- branch dan commit jika ada;
- file utama yang berubah;
- command yang benar-benar dijalankan dan hasilnya;
- acceptance criteria yang belum terbukti;
- blocker dan next allowed action.
