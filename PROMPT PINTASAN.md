# PINTASAN — DCI SEO Auditor

> Author: Mas Wondho — Duta Corpora Indonesia (DCI)
> Copyright © 2026 Duta Corpora Indonesia — All rights reserved

Panduan ini menjelaskan cara memanggil pipeline artikel dengan satu perintah, di agent mana pun.

## Dua cara memanggil

| Cara | Cocok untuk | Syarat |
|---|---|---|
| Command `/artikel` | TRAE, ZCode, Claude Code | Pasang sekali di komputer Anda (lihat bagian "Memasang `/artikel`") |
| Prompt biasa | Agent apa pun, termasuk Codex, Cursor, Gemini, dan agent yang belum terdaftar | Tidak ada. Cukup salin prompt di bawah |

### Cara 1: command `/artikel`

```text
/artikel <nama perusahaan> <bulan> [tahun]
```

Contoh:

```text
/artikel Salimah Catering November
/artikel Salimah Catering November 2026
```

### Cara 2: prompt biasa (berlaku di semua agent)

```text
Baca AGENT.md, lalu kerjakan <nama perusahaan> bulan <bulan> sesuai Section 10 (Mode Pintasan).
```

Prompt ini sama hasilnya dengan command. Bedanya, command sudah memuat langkah-langkah rinci, sedangkan prompt biasa mengandalkan agent membaca `AGENT.md` sendiri.

## Cara membaca argumen

- Kata terakhir adalah nama bulan.
- Bila kata terakhir berupa angka empat digit, itu tahun, dan nama bulan adalah kata sebelumnya.
- Semua kata di depannya adalah nama perusahaan. Boleh lebih dari satu kata.
- Argumen kosong atau tidak terbaca: agent bertanya, tidak menebak.

## Isi perintah dan maksudnya

Sumber perintah ada di `perintah/artikel.md` (satu berkas netral, bukan milik agent tertentu). Berikut arti tiap bagian:

| Bagian | Maksudnya |
|---|---|
| Argumen dari operator | Teks yang Anda ketik setelah `/artikel`: nama perusahaan, bulan, dan tahun |
| Cara membaca argumen | Aturan memisahkan nama perusahaan dari bulan dan tahun (lihat bagian di atas) |
| Lokasi project | Perintah dijalankan dari folder yang berisi `AGENT.md` dan `alat/`. Di luar folder itu, jalur relatif tidak ditemukan |
| Skill tidak wajib | Agent tidak boleh mengunduh skill dan tidak boleh berhenti bila skill tidak ada. Semua aturan ada di repo |
| Langkah 1 dan 2 | Membaca `AGENT.md` dan `aturan/kerja-tanpa-skill.md`, lalu mengikuti Mode Pintasan (Section 10) |
| Langkah 3 | Gerbang status: menentukan draft mana yang boleh dikerjakan. Hanya `BARU` dan `LANJUTKAN` |
| Langkah 4 | Audit draft mentah: daftar temuan bernomor sebagai bahan menulis ulang. Tidak pernah menghentikan pekerjaan |
| Langkah 5 | Menulis berkas `- Meta.txt`, lalu gerbang kualitas. Hanya bagian yang FAIL diperbaiki, tidak merombak seluruh artikel |
| Langkah 6 | Draft asli tidak ditimpa. Ledger dan laporan ditulis ke `LAPORAN.md`. Hash disalin dari keluaran skrip, tidak dihitung manual |
| Langkah 7 | Aturan bukti: kata "lulus" hanya boleh dipakai bila gerbang terbaru menunjukkan `0 FAIL` |
| Langkah 8 | Laporan akhir ke operator: status tiap draft, tabel artikel yang diproses, dan temuan yang butuh keputusan |

## Memasang `/artikel`

Berkas command tidak ikut repo, karena tiap agent punya format dan folder sendiri. Repo hanya membawa sumber netralnya (`perintah/artikel.md`) dan pemasang (`alat/pasang-perintah.py`). Jalankan sekali di komputer Anda, dari folder root project:

```text
python -I -X utf8 alat/pasang-perintah.py trae
```

| Perintah | Hasil |
|---|---|
| `... pasang-perintah.py --daftar` | Menampilkan agent yang didukung dan foldernya |
| `... pasang-perintah.py trae` | Pasang untuk TRAE di project ini |
| `... pasang-perintah.py trae zcode claude` | Pasang beberapa agent sekaligus |
| `... pasang-perintah.py semua` | Pasang ke semua agent yang didukung |
| `... pasang-perintah.py trae --global` | Pasang di folder rumah, berlaku di semua project |
| `... pasang-perintah.py trae --cek` | Hanya memeriksa apakah sudah terpasang dan terbaru |

Di macOS atau Linux, ganti `python` dengan `python3`. Setelah memasang, muat ulang agent atau buka sesi baru.

### Agent yang didukung

| Agent | Folder project | Argumen | Sumber format |
|---|---|---|---|
| TRAE | `.trae/commands/artikel.md` | Teks setelah `/artikel` | docs.trae.ai/ide/slash-commands |
| ZCode | `.zcode/commands/artikel.md` | Teks setelah `/artikel` | zcode.z.ai/en/newdocs/commands |
| Claude Code | `.claude/commands/artikel.md` | `$ARGUMENTS` | code.claude.com/docs/en/slash-commands |

Agent lain tidak punya folder command yang dipakai pemasang. Codex misalnya sudah menghapus custom prompts dan menggantinya dengan skills, jadi gunakan Cara 2 (prompt biasa).

### Bila perintah tidak muncul di menu `/`

- Pastikan agent dibuka dengan root project ini sebagai workspace (folder yang berisi `AGENT.md`).
- Jalankan `pasang-perintah.py <agent> --cek` untuk memastikan berkasnya ada dan terbaru.
- Muat ulang agent atau buka sesi baru. Perubahan command tidak selalu terbaca di sesi yang sedang berjalan.
- TRAE: cek Settings > Skills & Commands.
- Bila tetap tidak muncul, pakai Cara 2. Hasilnya sama.

### Setelah repo diperbarui

Isi `perintah/artikel.md` bisa berubah di versi baru. Jalankan ulang pemasang untuk memperbarui salinan di komputer Anda. Perintah `--cek` menunjukkan apakah salinan Anda sudah usang.

## Aturan memuat `AGENT.md`

`AGENTS.md` di repo ini sengaja pendek (±500 token) dan hanya menunjuk ke `AGENT.md` (aturan lengkap, ±8.000 token). Agent yang membaca `AGENTS.md` otomatis (TRAE bila opsi *Include AGENTS.md in the context* aktif di Settings > Rules & Memories, Codex, dan lainnya) hanya memuat penunjuk itu. `AGENT.md` dibuka saat tugasnya artikel.

## Yang terjadi setelah dikirim

1. Agent mencari folder perusahaan di `klien/` dan membaca `CLIENT.md`-nya.
2. Mencari folder bulan di `artikel/`, lalu menjalankan Gerbang Status pada semua draft.
3. Hanya draft `BARU` dan `LANJUTKAN` yang dikerjakan: audit, humanize, berkas meta, gerbang kualitas, lalu ZeroGPT.
4. Hasil: `<judul> - Humanized.txt` dan `<judul> - Meta.txt` per artikel, serta ledger dan laporan di `LAPORAN.md` folder bulan itu.
5. Laporan ringkas di chat, termasuk draft yang dilewati beserta alasannya.

## Kalau penulis mengerjakan bertahap

Aman dijalankan berulang kali. Gerbang Status membandingkan isi draft dengan ledger di `LAPORAN.md`:

| Status | Artinya | Yang dilakukan agent |
|---|---|---|
| `BARU` | Draft lengkap, belum pernah diaudit | Audit penuh |
| `MENUNGGU` | Draft belum lengkap (belum berakhir dengan shortcode WA klien) | Dilewati |
| `LANJUTKAN` | Pernah dikerjakan sebagian | Hanya tahap yang masih kosong |
| `SELESAI` | Semua tahap sudah tercatat | Dilewati, tidak diaudit ulang |
| `BERUBAH` | Penulis mengedit draft setelah diaudit | Berhenti dan bertanya ke operator |
| `TANPA-CATATAN` | Versi Humanized ada tetapi tidak tercatat di ledger | Dilewati dan dilaporkan |
| `RUSAK` | Berkas draft bukan UTF-8 | Dilewati, operator diminta menyimpan ulang sebagai UTF-8 |

Untuk memaksa audit ulang, tulis di akhir perintah: `Audit ulang [nama draft], alasannya: ...`.

## Syarat sebelum dipakai untuk klien baru

- Folder klien ada di `klien/` (salin dari `klien/_TEMPLATE/`) dan `CLIENT.md`-nya terisi lengkap (lihat `AGENT.md` Section 3). Isian bawaan template yang belum diganti ditolak skrip dengan pesan jelas.
- Draft mentah `.txt` ada di `klien/<Klien>/artikel/<tahun bulan>/`.
- Agent punya akses browser (untuk ZeroGPT). Bila gagal, agent menandai `MANUAL CHECK NEEDED`.

## Variasi opsional (tambahkan di akhir perintah)

- `Hanya audit, jangan humanize.` untuk melihat temuan saja.
- `Hanya file [nama draft].` untuk satu artikel.
- `Lewati ZeroGPT.` bila hanya butuh rewrite.
