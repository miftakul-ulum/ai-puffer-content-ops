# AGENTS.md — DCI SEO Auditor

> Author: Mas Wondho — Duta Corpora Indonesia (DCI)
> Copyright © 2026 Duta Corpora Indonesia — All rights reserved

Project ini mengerjakan artikel SEO WordPress untuk klien Duta Corpora Indonesia. Berkas ini sengaja pendek. Aturan lengkap ada di berkas lain, dan dibaca hanya saat tugasnya artikel.

## Kapan membaca aturan lengkap

Bila tugasnya mengerjakan, mengaudit, atau memeriksa artikel klien (`klien/<Nama Klien>/artikel/...`), baca dua berkas ini sebelum mulai:

1. `AGENT.md`: pipeline, checklist, aturan konten (Section 11), dan mode pintasan `/artikel` (Section 10).
2. `aturan/kerja-tanpa-skill.md`: metode menulis ulang, aturan fakta, disiplin bukti, berkas meta, dan aturan kanibalisasi.
3. Muat skill wajib dari folder `skills/` repo ini: `skills/dci-seo-auditor/SKILL.md` (induk), `skills/antislop-copywriting/SKILL.md` + `skills/antislop/SKILL.md` (Tahap humanize), dan `skills/verification-before-completion/SKILL.md` (sebelum klaim selesai). Pustaka SEO opsional (keluarga `blog`, `ai-seo`, `programmatic-seo`, `seo-audit`, `schema`, `site-architecture`, `competitors`, `competitor-profiling`, `content-strategy`, `directory-submissions`, `free-tools`, `marketing-tools`, `aso`) juga ada di `skills/` — pakai sesuai kebutuhan, tidak wajib.

Untuk tugas lain di repo ini (misalnya mengubah skrip di `alat/`), berkas di atas tidak perlu dibaca. Setelah mengubah skrip, jalankan `python -I -X utf8 alat/uji-tools.py`.

## Hal yang tidak boleh ditawar

- Skill wajib adalah skill yang ada di folder `skills/` repo ini. Muat dengan membaca `SKILL.md`-nya. Jangan mengunduh skill lain dari luar repo, dan jangan menyebut pekerjaan selesai bila skill wajib belum dimuat.
- Jangan menyatakan artikel lulus sebelum `python -I -X utf8 alat/cek-artikel.py "<artikel>"` (atau `python3 -I -X utf8 alat/cek-artikel.py "<artikel>"` di macOS/Linux) dijalankan pada berkas terbaru dan menunjukkan `0 FAIL`. Di macOS atau Linux pakai `python3`.
- Jangan mengarang statistik, testimoni, nama, harga, atau fakta kota. Tidak ada sumber, tidak ditulis.
- Draft asli tidak ditimpa. Hasil akhir disimpan sebagai `<nama> - Humanized.txt`.
- Data satu klien tidak boleh muncul di artikel klien lain.

## Menyapa operator

Cara menyapa mengikuti `AGENTS.md` atau persona yang ada di komputer masing-masing karyawan. Berkas ini tidak menetapkan nama sapaan.

## Menjalankan

Ketik `/artikel <nama perusahaan> <bulan> [tahun]` bila perintah sudah dipasang (`python -I -X utf8 alat/pasang-perintah.py --daftar` menunjukkan agent yang didukung). Di agent mana pun, cukup tulis: `Baca AGENT.md, lalu kerjakan <nama perusahaan> bulan <bulan> sesuai Section 10.` Panduan lengkap: `PROMPT PINTASAN.md`.
