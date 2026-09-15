# Stage 6 — Evidence-Based Evaluation

## Scope

Buat evaluator yang terpisah dari interviewer sesuai `../AI_SYSTEM.md`.

## Deliverables

- Lima dimensi rubric 0–5.
- `overall` dihitung oleh fungsi kode dengan bobot versioned.
- Schema ketat, exact evidence validation, dan provenance.
- Status `evaluated`, `needs_review`, atau `insufficient_answer`.
- Retry/failure handling yang membedakan jawaban lemah dari provider failure.
- Tests untuk range, formula, quote palsu, output rusak, kosong, retry, dan persistence.

## Gate

Semua skor valid, overall konsisten, quote dapat dibuktikan dari answer, dan provider failure tidak menjadi skor nol.
