---
name: dci-seo-auditor
description: Pipeline lengkap DCI SEO Auditor - memandu audit draft, humanize, gerbang kualitas, ZeroGPT, dan laporan artikel klien. Muat skill ini sebagai langkah pertama saat mengerjakan /artikel atau tugas artikel apa pun di repo ini.
---

# DCI SEO Auditor — Skill Induk Project

Skill ini adalah pintu masuk pipeline artikel. Ia tidak memuat aturan secara langsung; ia memandu
urutan membaca berkas aturan dan menjalankan alat, plus mewajibkan skill pendamping.

## Urutan wajib saat mengerjakan artikel

1. Baca `AGENT.md` (pipeline Section 4, checklist Section 5, protokol ZeroGPT Section 6,
   format laporan Section 7, aturan konten Section 11, mode pintasan Section 10).
2. Baca `aturan/kerja-tanpa-skill.md` (metode menulis ulang, tanda tulisan mesin, aturan fakta,
   disiplin bukti, berkas `- Meta.txt`, aturan kanibalisasi).
3. Muat skill pendamping WAJIB dari folder `skills/` repo ini (baca `SKILL.md`-nya):
   - `skills/antislop-copywriting/SKILL.md` — filter anti-deteksi inti (Tahap 3 humanize).
   - `skills/antislop/SKILL.md` — core antislop yang dirujuk antislop-copywriting.
   - `skills/verification-before-completion/SKILL.md` — wajib sebelum klaim selesai (Tahap 5).
4. Sebelum audit apa pun, jalankan Gerbang Status:
   `python -I -X utf8 alat/cek-status.py "klien/<Klien>/artikel/<YYYY Bulan>"`.
   Proses hanya draft `BARU` dan `LANJUTKAN`.
5. Audit draft mentah: `python -I -X utf8 alat/cek-artikel.py "<draft>" --draft`
   — daftar TEMUAN bernomor = bahan humanize.
6. Setelah humanize, tulis `<artikel> - Meta.txt`, lalu jalankan Gerbang Kualitas:
   `python -I -X utf8 alat/cek-artikel.py "<artikel>"` — wajib `0 FAIL` sebelum klaim selesai.
7. Pindai ZeroGPT sesuai `AGENT.md` Section 6, tulis `LAPORAN.md` (Section 7).

## Aturan yang tidak bisa ditawar

- Skill di `skills/` ini WAJIB dipakai (antislop-copywriting + antislop + verification-before-completion).
  Jangan mengunduh skill lain; bila komputer tidak punya mekanisme skill, baca berkas SKILL.md-nya
  sebagai berkas aturan biasa — hasilnya sama.
- Section 11 (`AGENT.md`) selalu menang atas preferensi skill generik.
- Draft asli tidak ditimpa; hasil = `<nama> - Humanized.txt`.
- Tidak ada klaim angka/fakta tanpa sumber. Tidak ada klaim selesai tanpa gerbang `0 FAIL`.

Author: Mas Wondho — Duta Corpora Indonesia (DCI)
Copyright © 2026 Duta Corpora Indonesia — All rights reserved
