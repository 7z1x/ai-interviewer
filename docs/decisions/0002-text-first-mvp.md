# ADR-0002 — MVP Interview Berbasis Teks

- Status: accepted
- Date: 2026-09-15

## Context

Voice, STT/TTS, dan avatar menambah biaya, latency, browser permission, privacy, serta failure mode yang tidak diperlukan untuk membuktikan inti produk.

## Decision

MVP sampai Stage 9 memakai interview teks. Voice dan avatar dikerjakan hanya sebagai tahap lanjutan setelah alur setup, interview, evaluation, report, persistence, security, dan observability terverifikasi.

## Consequences

- Portfolio lebih cepat membuktikan workflow AI dan evidence-based evaluation.
- UI dan domain tetap perlu dirancang agar voice dapat ditambahkan melalui adapter tanpa mengubah sumber kebenaran jawaban.
- Voice/avatar bukan acceptance criteria MVP.
