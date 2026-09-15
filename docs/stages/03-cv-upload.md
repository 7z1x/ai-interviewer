# Stage 3 — CV Upload and Extraction

## Scope

Upload satu PDF per session dan ekstrak text layer per halaman. Ikuti batas dan retensi di `../SECURITY.md`.

## Deliverables

- Validasi extension, MIME, magic bytes, 5 MiB, 10 halaman, enkripsi, dan parser result.
- Internal filename/path acak dan cleanup temporary/raw file sesuai ADR.
- Teks dan metadata halaman yang dapat ditelusuri.
- Status document serta endpoint upload/status.
- Fixture kecil dan automated failure tests.

## Do Not Build

OCR, embeddings, RAG, interview agent, voice, atau avatar.

## Gate

PDF valid berhasil; file palsu, besar, encrypted, kosong, dan rusak ditolak aman; path traversal tidak terjadi; session tetap konsisten saat parsing gagal.
