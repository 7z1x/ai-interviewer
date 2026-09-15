# Stage 4 — Candidate Context and Interview Plan

## Scope

Buat provider boundary dan plan lima pertanyaan dari CV, role, job description, serta bahasa.

## Deliverables

- `LLMProvider`, deterministic stub, dan adapter OpenCode tunggal.
- Verifikasi API aktual `opencode serve`; jangan mengasumsikan OpenAI compatibility.
- Structured output Pydantic dengan provenance skill/requirement.
- Session terisolasi, tools off, timeout/retry terbatas, dan cleanup.
- Plan persistence, idempotency/regenerate rule, serta readiness terpisah.
- Unit/integration/provider contract tests memakai stub atau mocked HTTP.

## Gate

Tepat lima pertanyaan memiliki competency/objective; unsupported skill ditolak; invalid output gagal aman; demo stub berjalan tanpa key; pergantian mode hanya melalui configuration.
