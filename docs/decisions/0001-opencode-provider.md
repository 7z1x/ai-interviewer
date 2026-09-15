# ADR-0001 — OpenCode sebagai LLM Gateway

- Status: accepted for implementation, runtime compatibility not yet verified
- Date: 2026-09-15

## Context

Project memerlukan provider AI yang dapat dipakai secara lokal maupun melalui server terautentikasi, tanpa menyebarkan detail transport ke business logic.

## Decision

Gunakan interface `LLMProvider`, `StubLLMProvider` untuk test/demo deterministik, dan satu `OpenCodeProvider` sebagai adapter HTTP ke `opencode serve`. Endpoint dan payload aktual diverifikasi pada Stage 4 terhadap versi OpenCode yang digunakan. Jangan menganggapnya kompatibel dengan OpenAI API.

Session aplikasi harus terisolasi, tools dimatikan, output diminta terstruktur, timeout/retry dibatasi, dan session sementara dibersihkan.

## Consequences

- Business logic tidak berubah ketika base URL/provider berubah.
- Automated test tidak membutuhkan OpenCode atau API key.
- Adapter memerlukan contract test dan live smoke test terpisah.
- OpenCode tetap dapat memakai provider online; project tidak boleh mengklaim inference offline tanpa bukti konfigurasi.
