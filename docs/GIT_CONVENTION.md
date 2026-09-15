# Git Convention — AI Interviewer

> Sumber kebenaran penamaan. Menggantikan `feat(stage-N)` di dokumen lama.

## Branch
- `feat/<feature-kebab>` untuk fitur baru
- `fix/<feature>-<issue>` untuk bugfix setelah merge
- `docs/<topic>` untuk dokumentasi murni
- Contoh: `feat/db-session`, `fix/upload-mime-validation`, `docs/prd-convention`

## Commit
- Title: `type(scope): subject` — type = feat|fix|docs|chore|refactor
- Scope = fitur, bukan stage number
- Body wajib: `Stage N — <Nama>` + ringkasan AC yang di-verify
- Contoh:
```
feat(upload): validate PDF and extract text per page

Stage 3 — CV Upload and Extraction
AC: file palsu/besar/terenkripsi ditolak 422, pg extraction ok
```

## PR
- Title: `feat(scope): subject` (sama kayak commit)
- Description template:
```
Stage N — <Nama>
Prompt: docs/AI_INTERVIEWER_STEP_BY_STEP_PROMPTS.md#Prompt N
Branch: feat/<feature> -> main
AC:
- [x] ...
- [ ] ...
Commands:
- ruff check ... -> pass
- pytest ... -> 3 passed
Blocker: none / ...
```
- Merge: squash atau merge --no-ff, jangan force push. Setelah merge, cek conflict dengan main via `git fetch && git merge-tree $(git merge-base main HEAD) main HEAD`, resolve trivial langsung, tanya user jika kritis.
