# Hermes Runbook — AI Interviewer

Dokumen ini hanya menjelaskan cara menjalankan stage melalui Hermes. Aturan engineering permanen berada di root `AGENTS.md`; scope dan acceptance criteria berada di `docs/stages/`.

## Prerequisites

- Repository sudah di-clone pada runtime Hermes.
- Hermes mengetahui repository URL, default branch, dan working directory aktual.
- Credential tersedia melalui secret store/environment runtime, bukan dikirim melalui WhatsApp.
- Jangan mengirim GitHub token, API key, password, `.env`, CV, atau data sensitif melalui chat.

Hermes yang berjalan di server tidak dapat membaca path Windows pengguna secara langsung.

## Execution Contract

- Kerjakan tepat satu stage yang diminta pengguna.
- Sebelum mengedit: periksa repository, remote, branch, working tree, `AGENTS.md`, dokumen desain terkait, dan `docs/EXECUTION_STATUS.md`.
- Tahap sebelumnya harus berstatus `verified` sebelum tahap baru dimulai.
- Tarik perubahan remote hanya jika working tree aman.
- Gunakan branch `feat/ai-interviewer-stage-XX` kecuali pengguna menentukan branch lain.
- Satu hari berarti satu stage aktif, bukan kewajiban menyelesaikannya dengan mengorbankan verifikasi.
- Jangan mengubah scope, provider, atau arsitektur terkunci tanpa keputusan pengguna/ADR.
- Jangan deploy production, membeli layanan, membuat akun, mengubah DNS, atau menerima ketentuan legal.
- Commit hanya jika diminta dan quality gates stage lulus. Push hanya jika pengguna menulis `PUSH` secara eksplisit.
- Setelah laporan dikirim, berhenti dan tunggu instruksi berikutnya.

## Daily Prompt

Ganti seluruh placeholder sebelum dikirim:

```text
Lanjutkan project AI Interviewer.

Repository: <REPOSITORY_URL>
Working directory runtime: <WORKING_DIRECTORY>
Stage hari ini: <STAGE_NUMBER> dari docs/stages/<STAGE_FILE>.md
Git action akhir: <COMMIT ATAU JANGAN COMMIT>; <PUSH ATAU JANGAN PUSH>

Sebelum bekerja:
1. Pastikan repository, remote, branch, dan working directory benar.
2. Baca AGENTS.md, file stage, dokumen desain terkait, dan docs/EXECUTION_STATUS.md.
3. Pastikan stage sebelumnya verified dan working tree aman.

Kerjakan hanya scope stage tersebut dan buktikan acceptance criteria-nya.
Jangan membuka/menampilkan secret atau data pribadi.
Jangan lanjut ke stage berikutnya.

Setelah bekerja:
1. Jalankan quality gates yang tersedia dan relevan.
2. Perbarui docs/EXECUTION_STATUS.md secara jujur.
3. Ikuti instruksi Git di atas; jangan menebaknya.
4. Laporkan status, branch/commit, file berubah, command dan hasil aktual,
   acceptance criteria yang belum terbukti, blocker, dan next allowed action.
```

## Blocker Handling

Jika terhalang credential, layanan eksternal, keputusan arsitektur, konflik perubahan, atau kegagalan berulang, jangan mengarang solusi/hasil. Catat bukti yang sudah diperiksa, tandai stage `in_progress` atau `blocked` secara jujur, lalu berhenti pada batas kewenangan.

## Execution Status Template

```md
# Execution Status

## Current State
- Current stage: ...
- Status: pending | in_progress | verified | blocked
- Branch: ...
- Base commit: ...
- Last verified commit: ...
- Updated at: ... UTC

## Last Verified Commands
- Command: ...
- Result: ...

## Open Blockers
- None | ...

## Next Allowed Action
- ...
```
