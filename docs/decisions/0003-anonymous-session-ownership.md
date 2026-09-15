# ADR-0003 — Anonymous Session Ownership

- Status: proposed; finalize before persistence/API implementation
- Date: 2026-09-15

## Context

MVP tidak mempunyai akun, tetapi CV, jawaban, score, dan report merupakan data sensitif. UUID session tidak cukup sebagai bukti kepemilikan.

## Decision

Gunakan random opaque owner token. Browser menerima token melalui cookie `HttpOnly`; backend menyimpan hash token dan memverifikasinya pada setiap operasi session. Production cookie memakai `Secure` dan kebijakan `SameSite` yang sesuai flow.

## Consequences

- Endpoint tidak boleh mengandalkan session ID saja.
- Perlu desain bootstrap/recovery token, CSRF review, expiry, deletion, dan test unauthorized access.
- Detail final harus disepakati sebelum Stage 2 mengunci schema dan sebelum endpoint membawa data nyata.
