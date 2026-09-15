# ADR-0004 — Raw CV Dihapus Setelah Ekstraksi

- Status: proposed; validate against product needs before Stage 3
- Date: 2026-09-15

## Context

MVP membutuhkan text layer CV untuk membuat plan, tetapi tidak membutuhkan raw PDF setelah ekstraksi berhasil. Menyimpan raw file memperbesar risiko privasi dan beban storage.

## Decision

Hapus raw PDF setelah extracted text per halaman berhasil dipersist dan diverifikasi. Simpan extracted text serta data session maksimal 30 hari, kemudian hapus melalui cleanup job idempotent.

## Consequences

- User perlu upload ulang jika ekstraksi harus diulang dari sumber asli.
- Tidak ada preview/download CV setelah raw file dihapus.
- Cleanup dan audit metadata perlu diuji.
- Jika raw storage diperlukan kemudian, buat ADR pengganti dengan encryption, access control, dan retention yang eksplisit.
