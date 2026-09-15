# Stage 5 — LangGraph Text Interview

## Scope

Implementasikan workflow teks dengan state yang tersimpan dan dapat dipulihkan.

## Deliverables

- State dan node sesuai `../ARCHITECTURE.md`.
- Maksimal lima pertanyaan utama dan satu follow-up per pertanyaan.
- Endpoint start, current question, submit answer, next, dan end.
- Idempotent submission dan recovery setelah restart.
- Graph tests untuk jalur cukup, vague, limit, complete, restart, dan duplicate.

## Do Not Build

Final scoring, voice, avatar, atau UI kompleks.

## Gate

Workflow deterministik dalam stub mode, seluruh transition penting diuji, state recoverable, dan batas tidak dapat dilewati.
