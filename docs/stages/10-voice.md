# Stage 10 — Optional Voice

## Scope

Tambahkan input/output voice tanpa mengubah sumber kebenaran jawaban teks.

## Deliverables

- ADR pemilihan MediaRecorder/WebSocket/WebRTC dan STT/TTS berdasarkan bukti biaya, latency, privacy, browser support, dan kompleksitas.
- Provider interface + stub dan fixture audio.
- State permission/listening/processing/speaking/error.
- Transcript terlihat dan dapat dikoreksi sebelum submit.
- Fallback teks selalu tersedia.

## Gate

Mic ditolak atau provider gagal tidak merusak session; user dapat melanjutkan via teks; transcript terkonfirmasi sebelum menjadi answer final.
