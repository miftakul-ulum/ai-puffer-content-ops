# DCI SEO Auditor: Agentic SEO Auditor by Duta Corpora Indonesia

DCI SEO Auditor mengubah draft artikel mentah dari plugin AI Puffer menjadi artikel WordPress yang siap tayang. Agent mengerjakan audit, penulisan ulang, dan pemeriksaan. Dua skrip Python menjadi gerbang yang memutuskan lulus atau tidaknya, jadi hasilnya tidak bergantung pada penilaian agent sendiri.

Tool ini dibuat untuk karyawan Duta Corpora Indonesia. Cara agent menyapa operator mengikuti `AGENTS.md` atau persona di komputer masing-masing.

Target tiap artikel: skor Rank Math 80 sampai 100, bahasa Indonesia baku, lolos ZeroGPT, dan tercatat per klien.

```text
draft mentah ──► GERBANG STATUS ──► AUDIT ──► HUMANIZE ──► GERBANG KUALITAS ──► ZeroGPT ──► LAPORAN
                                                                  │
                                       perbaiki hanya bagian FAIL ◄┘
```

## Yang dijamin dan yang tidak

Gerbang kualitas membuktikan bahwa artikel memenuhi aturan format dan bahasa di repo ini: jumlah kata, keyword, heading, format WordPress, judul SEO dan slug, ejaan, serta tidak ada kalimat yang disalin dari artikel lain. Lulus berarti `0 FAIL`.

Gerbang tidak menjamin peringkat. Skor Rank Math adalah skor plugin, bukan sinyal Google. Google tidak menetapkan jumlah kata atau jumlah keyword, dan melarang pengulangan yang terdengar tidak wajar (`FAKTA-SEO.md`). Target 31 sampai 34 kali keyword adalah aturan template kita sendiri. Hasil di Google hanya bisa dinilai dari data Search Console klien.

## Cara kerja

1. **Gerbang status.** `cek-status.py` membandingkan sidik jari isi draft dengan ledger di `LAPORAN.md`. Draft yang sudah diaudit tidak diaudit dua kali, dan draft yang masih ditulis penulis dilewati.
2. **Audit.** `cek-artikel.py --draft` mengeluarkan daftar temuan bernomor: komponen wajib, ejaan tidak baku, kata asing, angka tanpa label, dan pola khas tulisan AI. Audit ini tidak pernah menghentikan pekerjaan (exit 0).
3. **Humanize.** Agent menulis ulang berdasarkan daftar temuan dan `aturan/kerja-tanpa-skill.md`. Statistik, testimoni, dan nama tidak boleh dikarang.
4. **Gerbang kualitas.** `cek-artikel.py` memeriksa artikel dan berkas `- Meta.txt` pendampingnya. Artikel lulus bila hasilnya `0 FAIL`.
5. **ZeroGPT dan laporan.** Hasil dipindai di ZeroGPT, lalu angkanya dicatat apa adanya di `LAPORAN.md` klien.

### Status draft

| Status | Artinya |
|---|---|
| `BARU` | Draft lengkap, belum pernah diaudit |
| `MENUNGGU` | Draft belum lengkap, penulis masih bekerja |
| `LANJUTKAN` | Pernah dikerjakan sebagian, hanya tahap yang kosong dilanjutkan |
| `SELESAI` | Semua tahap tercatat, tidak diaudit ulang |
| `BERUBAH` | Draft diedit setelah diaudit, agent bertanya ke operator |
| `TANPA-CATATAN` | Versi Humanized ada tetapi tidak tercatat di ledger |
| `RUSAK` | Berkas bukan UTF-8, perlu disimpan ulang |

### Kode keluar `cek-artikel.py`

| Kode | Artinya |
|---|---|
| `0` | Tidak ada FAIL |
| `1` | Ada FAIL: perbaiki bagian yang gagal |
| `2` | Masukan tidak bisa diperiksa: berkas tidak ada, bukan UTF-8, keyword tidak terdeteksi, atau `CLIENT.md` belum diisi |

## Struktur

```text
.
├── AGENTS.md                # penunjuk pendek (±500 token) yang dimuat agent otomatis
├── AGENT.md                 # aturan kerja: pipeline, checklist, protokol, template prompt
├── FAKTA-SEO.md             # fakta Google dan Rank Math, lengkap sumber dan tanggal
├── aturan/
│   └── kerja-tanpa-skill.md # aturan kerja mandiri, tanpa skill apa pun
├── PROMPT PINTASAN.md       # panduan /artikel, isi perintah, cara memasang, prompt cadangan
├── CHANGELOG.txt            # riwayat perubahan sistem
├── CLAUDE.md                # impor AGENTS.md untuk Claude Code
├── perintah/
│   └── artikel.md           # sumber netral command /artikel (tanpa format khusus agent)
├── alat/
│   ├── cek-status.py        # gerbang status draft
│   ├── cek-artikel.py       # audit draft dan gerbang kualitas final
│   ├── pasang-perintah.py   # memasang /artikel ke TRAE, ZCode, atau Claude Code
│   ├── kamus-kata.txt       # kamus kata sah hasil tinjauan manual (diperluas bertahap)
│   ├── kamus-kbbi-offline.txt # wordlist KBBI offline, 112.651 kata, tanpa jaringan
│   └── uji-tools.py         # uji otomatis semua skrip
└── klien/                   # semua data klien ada di sini
    ├── _TEMPLATE/           # cetakan klien baru
    └── <Nama Klien>/
        ├── CLIENT.md        # data klien
        └── artikel/<YYYY Bulan>/
            ├── <slug>.txt              # draft mentah (arsip, tidak ditimpa)
            ├── <slug> - Humanized.txt  # hasil akhir, siap tempel ke WordPress
            ├── <slug> - Meta.txt       # judul SEO, deskripsi meta, slug
            └── LAPORAN.md              # ledger dan laporan bulan itu
```

Folder berawalan `_` bukan klien dan tidak pernah diproses. Folder milik agent (`.trae/`, `.zcode/`, `.claude/`, `.agents/`, dan sejenisnya) ada di `.gitignore` dan tidak ikut repo. Semua yang dibutuhkan pipeline ada di `alat/`, `aturan/`, `perintah/`, dan `klien/`, sehingga bekerja di agent mana pun.

## Memulai

Butuh agent apa pun yang bisa membaca berkas biasa (TRAE, ZCode, Claude Code, Codex, dan lainnya) dan Python 3.8 ke atas. Tidak perlu memasang skill: semua aturan ada di repo ini (`aturan/kerja-tanpa-skill.md`). Di Windows, jalankan skrip dengan `python`. Contoh di dokumen memakai `python3`.

1. **Daftarkan klien.** Salin `klien/_TEMPLATE/` menjadi `klien/<Nama Klien>/`, ganti nama folder `YYYY Bulan` menjadi bulan kerja, lalu isi semua field di `CLIENT.md`. Isian bawaan template yang belum diganti ditolak skrip.
2. **Taruh draft.** Simpan draft mentah dari AI Puffer di `klien/<Nama Klien>/artikel/<YYYY Bulan>/<judul>.txt`.
3. **Pasang perintah** (sekali per komputer, hanya bila ingin memakai `/artikel`): `python -I -X utf8 alat/pasang-perintah.py trae` (atau `zcode`, `claude`, `semua`). Berkas command tidak ikut repo karena tiap agent punya format sendiri. Rinciannya di `PROMPT PINTASAN.md`.
4. **Jalankan** dengan root project sebagai workspace.
   - Dengan command: `/artikel Salimah Catering November`. Untuk TRAE, pastikan opsi *Include AGENTS.md in the context* aktif di Settings > Rules & Memories.
   - Agent mana pun, tanpa command: `Baca AGENT.md, lalu kerjakan Salimah Catering bulan November sesuai Section 10.`
5. **Ambil hasil.** `<judul> - Humanized.txt` siap ditempel ke editor WordPress. `LAPORAN.md` memuat metrik, angka ZeroGPT, dan catatan risiko. Isi `- Meta.txt` dimasukkan ke kolom judul SEO, deskripsi meta, dan permalink di Rank Math.

## Alat bawaan

| Perintah | Fungsi |
|---|---|
| `python3 -I alat/cek-status.py "klien/<klien>/artikel/<bulan>"` | Klasifikasi draft sebelum dikerjakan |
| `python3 -I -X utf8 alat/cek-artikel.py "<draft>" --draft` | Audit draft mentah, keluar daftar temuan |
| `python3 -I -X utf8 alat/cek-artikel.py "<artikel>"` | Gerbang kualitas final, exit 1 bila ada FAIL |
| `python3 -I -X utf8 alat/pasang-perintah.py trae` | Pasang `/artikel` ke TRAE. Lainnya: `zcode`, `claude`, `semua`, `--daftar`, `--cek` |
| `python3 -I -X utf8 alat/uji-tools.py` | Uji otomatis semua skrip (71 uji). Jalankan setelah mengubah skrip |

Verifikasi bahasa berjalan **sepenuhnya offline dan berlapis**: kamus approved (`kamus-kata.txt`, diperluas bertahap setelah tinjauan manual), lalu wordlist KBBI offline (`kamus-kbbi-offline.txt`, 112.651 kata, kata berimbuhan dinormalisasi ke bentuk dasar dulu). Tidak ada panggilan jaringan — situs KBBI Daring dan kbbi.web.id sama-sama dibatasi kuota (terverifikasi 2026-11-20), sehingga sengaja tidak dipakai. Kata yang tidak ditemukan di kedua lapisan dilaporkan sebagai *kata tidak terverifikasi* untuk tinjauan manual; kata yang memang baku ditambahkan ke `kamus-kata.txt`.

## ZeroGPT

Versi final dipindai di <https://www.zerogpt.com/>. Targetnya verdict *Human written* dengan AI di bawah 10%. Batas gratis 15.000 karakter, jadi blok editor dibuang dulu sebelum teks ditempel. Bila lebih panjang, teks dipecah di batas paragraf dan kedua angkanya dilaporkan. Plagiarisme belum punya alat cek otomatis. Gerbang kualitas hanya menangkap kalimat yang disalin antar artikel di repo ini.

## Contoh

Artikel *Jasa Catering Instansi Blitar* milik Salimah Catering: 2.073 kata, keyword 31 kali (density 1,50%), gerbang `0 FAIL 0 WARN`. Angka ZeroGPT (AI 3,7%, *Human written*) berasal dari catatan di `LAPORAN.md` dan belum diverifikasi ulang. Rinciannya ada di `klien/Salimah Catering/artikel/2026 November/LAPORAN.md`.

## Batasan yang diketahui

- `/artikel` belum diuji dari menu TRAE. Formatnya meniru command TRAE yang sudah ada.
- Opsi *Include AGENTS.md in the context* di TRAE adalah pengaturan per komputer, tidak bisa dibagikan lewat repo.
- Ambang kalimat yang disalin (3 rangkaian 8 kata) belum dikalibrasi pada artikel nyata lebih dari satu klien.
- Wordlist offline berasal dari turunan KBBI Daring (repo `damzaky/kumpulan-kata-bahasa-indonesia-KBBI`) dan mungkin tidak memuat istilah terbaru; kata yang tidak ada di wordlist tetap bisa baku — tinjau manual lalu tambahkan ke `kamus-kata.txt`.

---

Author: Mas Wondho — Duta Corpora Indonesia (DCI)
Copyright © 2026 Duta Corpora Indonesia — All rights reserved
