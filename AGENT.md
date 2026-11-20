# AGENT.md — DCI SEO Auditor (Agentic SEO Auditor by Duta Corpora Indonesia)

> Author: Mas Wondho — Duta Corpora Indonesia (DCI)
> Copyright © 2026 Duta Corpora Indonesia — All rights reserved
> Sumber aturan konten: Section 11 file ini (template prompt AI Puffer, GLOBAL, tanpa hardcode klien).
> File ini = otak project: format registry klien, pipeline kerja, checklist audit, protokol crosscheck, dan mode pintasan.
> File ini bersifat STATIS: tidak menyimpan data klien maupun laporan kerja. Keduanya hidup di folder masing-masing klien.

## 1. Tujuan Project

Tool ini dibuat untuk karyawan Duta Corpora Indonesia. Kata "operator" di dokumen ini berarti karyawan yang sedang menjalankan tool. Cara agent menyapa operator mengikuti `AGENTS.md` atau persona di komputer masing-masing, bukan file ini.

Menghasilkan artikel SEO WordPress siap publish untuk klien yang menggunakan plugin **AI Puffer**. Alur lengkap: draft mentah dari AI model → audit terhadap rules → parafrase/humanize (goal: lolos AI detector, human score 90%+) → verifikasi RankMath 80–100 → crosscheck ZeroGPT → final.

Template prompt di Section 11 sengaja **klien-global** (100% placeholder `{client_*}`). Data klien asli diisi dari `CLIENT.md` di folder klien (format di Section 3) — tidak pernah di-hardcode ke template maupun ke file ini.

## 2. Struktur Folder

```
[ROOT]/
├── AGENT.md                      ← file ini (pipeline + checklist, TANPA data klien)
├── PROMPT PINTASAN.md            ← panduan memanggil Mode Pintasan
├── FAKTA-SEO.md                  ← fakta Google/Rank Math bersumber + tanggal (wajib rujuk)
├── AGENTS.md                     ← penunjuk pendek ke berkas ini, dimuat agent otomatis (jaga tetap pendek)
├── aturan/kerja-tanpa-skill.md   ← aturan kerja mandiri, tanpa skill apa pun (Section 9)
├── perintah/artikel.md           ← sumber NETRAL command /artikel, tanpa format khusus agent (Section 10)
├── alat/pasang-perintah.py       ← memasang /artikel ke TRAE, ZCode, atau Claude Code di komputer ini
├── alat/cek-status.py            ← gerbang status: klasifikasi draft sebelum audit (Section 4)
├── alat/cek-artikel.py           ← gerbang kualitas: Rank Math + format WP + Anti-Typo (Section 4)
├── alat/kamus-kata.txt           ← kamus kata sah hasil tinjauan manual + verifikasi
├── alat/kamus-kbbi-offline.txt   ← wordlist KBBI offline (112.651 kata), lapisan verifikasi bahasa
├── alat/uji-tools.py             ← uji otomatis semua skrip (jalankan setelah mengubah skrip)
└── klien/                        ← SEMUA data klien hidup di sini, tidak ada di ROOT
    ├── _TEMPLATE/                ← cetakan klien baru (salin utuh, jangan dikerjakan langsung)
    │   ├── CLIENT.md
    │   └── artikel/YYYY Bulan/LAPORAN.md
    └── <Nama Klien>/
        ├── CLIENT.md             ← registry data klien tersebut (template di Section 3)
        └── artikel/
            └── <YYYY Month>/     ← contoh: "2026 November"
                ├── <Slug>.txt        ← draft mentah dari AI model (arsip, jangan ditimpa)
                ├── <Slug> - Humanized.txt ← hasil parafrase final siap paste ke WordPress
                └── LAPORAN.md    ← laporan audit + crosscheck bulan itu (Section 7)
```

Folder berawalan `_` (mis. `_TEMPLATE`) bukan klien: jangan pernah dikerjakan atau dicocokkan sebagai klien.

Folder milik agent (`.trae/`, `.zcode/`, `.claude/`, `.agents/`, dan sejenisnya) ada di `.gitignore` dan tidak ikut repo. Semua yang dibutuhkan pipeline ada di `alat/`, `aturan/`, `perintah/`, dan `klien/`. Jangan menaruh skrip atau aturan di folder agent.

## 3. Client Registry (Format Generik)

File ini **tidak menyimpan data klien manapun** — klien bisa banyak, jadi satu klien = satu folder = satu `CLIENT.md` di dalam folder itu. Semua placeholder `{client_*}` di Section 11 diisi dari `CLIENT.md` milik folder klien yang sedang dikerjakan.

**Klien baru:** salin `klien/_TEMPLATE/` menjadi `klien/<Nama Klien>/`, ganti nama folder `YYYY Bulan` sesuai bulan kerja, lalu isi `CLIENT.md`. Isi template ada di bawah (sumber salinan: `klien/_TEMPLATE/CLIENT.md`).

**Template `CLIENT.md`:**

| Field Placeholder | Isi |
|---|---|
| `{client_name}` | [nama bisnis klien] |
| `{client_url}` | [https://domain-klien] |
| `{client_business}` | [deskripsi bisnis 1 baris] |
| `{client_niche}` | [niche + wilayah operasi] |
| `{client_wa_shortcode}` | [shortcode tombol WA dari AI Puffer, mis. `[whatsapp_button id="..."]`] |
| Istilah dipertahankan | [opsional: istilah brand/produk yang boleh tetap mengikuti klien, pisah koma] |
| `{client_phone}` | [nomor WA/telepon + format wa.me/tel: ] |
| `{client_email}` | [email resmi] |
| Pola URL artikel | `{client_url}/artikel/[slug]` (sesuaikan bila klien beda pola) |
| Halaman layanan | [URL halaman layanan klien] |
| Gambar uploads | `{client_url}/wp-content/uploads/YYYY/MM/` |

**Aturan registry:**
1. Klien baru = buat folder baru + salin template `CLIENT.md` + isi data. DILARANG menambah data klien ke file ini atau mengedit Section 11.
2. Isolasi mutlak: dalam satu artikel, semua link internal & referensi hanya mengarah ke layanan klien aktif; dilarang menyebut/menautkan klien lain.
3. Data di `CLIENT.md` hanya berlaku untuk folder klien itu, bukan konfigurasi global.

## 4. Pipeline Kerja (5 Tahap + Gerbang Status)

### Tahap 1 — Draft
AI model menghasilkan draft mentah sesuai Section 11. Simpan apa adanya sebagai arsip (jangan ditimpa).

Penulis sering mengerjakan artikel bertahap: draft bisa belum selesai, atau diedit lagi setelah diaudit. Karena itu setiap draft melewati Gerbang Status di bawah sebelum disentuh.

### Gerbang Status — WAJIB sebelum Tahap 2
Jalankan: `python3 -I alat/cek-status.py "klien/<Klien>/artikel/<YYYY Bulan>"` (hanya membaca). Skrip membandingkan sidik jari isi draft dengan tabel ledger di `LAPORAN.md` (Section 7), lalu memberi satu status per draft:

| Status | Arti | Tindakan |
|---|---|---|
| `BARU` | Draft lengkap (baris terakhir = shortcode WA klien), belum ada di ledger | Audit penuh, mulai Tahap 2 |
| `MENUNGGU` | Draft belum lengkap, baris terakhir bukan shortcode WA. Penulis masih bekerja | Lewati. Lapor "belum lengkap", jangan diaudit |
| `LANJUTKAN` | Ada di ledger, isi tidak berubah, tetapi sebagian tahap masih `-` | Kerjakan hanya tahap yang `-`. Tahap yang sudah bertanggal dilarang diulang |
| `SELESAI` | Ada di ledger, isi tidak berubah, semua tahap terisi | Lewati. Dilarang diaudit ulang |
| `BERUBAH` | Ada di ledger, tetapi isi draft sudah berbeda dari yang diaudit | Jangan diproses otomatis. Lapor ke operator dan tanya apakah diaudit ulang. Hasil Humanized yang ada tidak boleh ditimpa tanpa persetujuan |
| `TANPA-CATATAN` | Versi Humanized sudah ada tetapi draft tidak tercatat di ledger | Jangan disentuh. Lapor ke operator, dan catat di ledger hanya atas persetujuan operator |
| `RUSAK` | Berkas draft bukan UTF-8 sehingga tidak bisa dibaca | Jangan diproses. Minta operator menyimpan ulang berkas sebagai UTF-8. Draft lain di folder yang sama tetap dinilai seperti biasa |

Berkas pendamping `<nama> - Humanized.txt` dan `<nama> - Meta.txt` bukan draft dan tidak dinilai. Bila `CLIENT.md` masih berisi isian bawaan template, skrip berhenti dengan pesan jelas: isi dulu semua field.

Aturan gerbang:
1. Hash di ledger hanya boleh disalin dari output skrip. Dilarang menghitung manual (`sha256sum` shell menghasilkan nilai berbeda karena cara normalisasinya lain, dan itu akan membuat semua draft tampak `BERUBAH`).
2. Tulis baris ledger segera setelah tiap tahap selesai (bukan menunggu semua selesai), supaya pekerjaan yang terputus bisa dilanjutkan tanpa mengulang.
3. Audit ulang hanya dengan perintah eksplisit operator. Sebutkan di laporan bahwa itu audit ulang beserta alasannya.
4. Status `BARU` bergantung pada shortcode WA di `CLIENT.md`. Draft yang memang lengkap tetapi tidak berakhir dengan shortcode akan terbaca `MENUNGGU`: itu kesalahan arah yang aman (menahan), dan operator bisa memintanya diproses.

### Tahap 2 — Audit (checklist terhadap draft mentah)
Jalankan: `python3 -I -X utf8 alat/cek-artikel.py "<draft mentah>" --draft`
Output = daftar TEMUAN bernomor (kompomen wajib, ejaan, kata asing, pola khas AI: ritme paragraf seragam,
variasi kalimat, marker percakapan berlebih, rule-of-three, angka tanpa label, kata di luar kamus).
Daftar itu = bahan kerja Tahap 3. Mode audit selalu exit 0 (laporan, bukan penghalang).

### Tahap 3 — Parafrase / Humanize
Tulis ulang sebagai "penulis manusia", bukan edit kosmetik:
- Variasi panjang kalimat: pendek (5–8 kata), sedang (12–18), sesekali panjang (20–30). Tanpa pola seragam.
- Variasi panjang paragraf (1–7 kalimat); tanpa dua paragraf berurutan berawalan kata sama.
- Marker percakapan maks 1–2× per artikel: "nah," "jujur saja," "sebenarnya," "kalau menurut pengalaman," "percaya atau tidak," + sapaan pembaca ("anda pasti pernah...", "coba bayangkan...", "mungkin anda bertanya-tanya...").
- Storytelling + detail realistis (skenario, kisaran biaya berlabel "kisaran"/"tergantung"). **Dilarang mengarang** statistik, testimoni, nama klien, penghargaan, atau tahun pengalaman.
- Dilarang: em dash, formula "bukan hanya X, tetapi Y", rule-of-three paksa, rangkaian fragmen staccato, cliché terlarang (daftar di Section 11).
- "Anda" kapital hanya di awal kalimat; selebihnya lowercase "anda".
- EYD/PUEBI: "silakan" (bukan "silahkan"), dsb.
- Bahasa Indonesia baku untuk seluruh prosa: kata asing yang ada padanan baku di KBBI ditulis ulang
  (contoh terverifikasi: snack box → kotak kudapan, nasi box → nasi kotak, dessert → pencuci mulut,
  coffee break → rehat kopi, partner → mitra, capcay → capcai). Yang DIPERTAHANKAN apa adanya: nama
  brand, fokus keyword, label/shortcode bawaan template, URL/atribut HTML, dan istilah pada baris
  "Istilah dipertahankan" di CLIENT.md.
- Klaim faktual (harga, nama masakan, kebiasaan kota, jumlah) wajib ada sumber: situs klien atau
  referensi nyata. Tidak bisa dicek → jangan tulis angkanya (kewajiban fact-check Google, FAKTA-SEO.md).

Selesai humanize: isi kolom Humanize di ledger dengan tanggal.

### Tahap 4 — Verifikasi SEO (Rank Math 80–100)
Tulis dulu berkas pendamping `<artikel> - Meta.txt` (judul SEO, deskripsi meta, slug; format di `aturan/kerja-tanpa-skill.md` bagian 5).
Jalankan gerbang kualitas: `python3 -I -X utf8 alat/cek-artikel.py "<artikel Humanized>"`.
Skrip memeriksa jumlah kata, paragraf pertama, jumlah/density/bold keyword, heading, format WordPress
(more-tag, nbsp, list, alt, shortcode, kontak), judul SEO/deskripsi meta/slug, kanibalisasi dan kalimat
yang disalin dari artikel lain di `klien/`, Anti-Typo Gate (ejaan tidak baku, kata asing, em dash,
"Anda" kapital), dan keluar exit 1 bila ada FAIL. Perbaiki hanya bagian yang gagal, jangan rombak.
Verifikasi bahasa berjalan OFFLINE dan berlapis: kata dicek ke kamus approved (`alat/kamus-kata.txt`)
lalu ke wordlist KBBI offline (`alat/kamus-kbbi-offline.txt`, 112.651 kata; kata berimbuhan dinormalisasi
ke bentuk dasar dulu). Tidak ada panggilan jaringan di gerbang — KBBI Daring dan kbbi.web.id keduanya
dibatasi kuota (terverifikasi 2026-11-20), jadi sengaja tidak dipakai. Kata yang tidak ditemukan di
kedua lapisan dilaporkan sebagai kata tidak terverifikasi (tinjauan manual, atau tambahkan ke kamus
bila memang baku).

Kode keluar `cek-artikel.py`: `0` tidak ada FAIL, `1` ada FAIL, `2` masukan tidak bisa diperiksa (berkas tidak ada, bukan UTF-8, keyword tidak terdeteksi, atau `CLIENT.md` belum diisi). Kode `2` bukan FAIL artikel: perbaiki masukannya, lalu jalankan ulang.
Fakta Google/Rank Math yang menjadi dasar ambang ada di `FAKTA-SEO.md` — rujuk situ, jangan ingatan.

### Tahap 5 — Crosscheck ZeroGPT + Final
Uji ke ZeroGPT (protokol di Section 6), isi kolom ZeroGPT di ledger (mis. `3,72% AI`) dan blok laporan di `LAPORAN.md` folder bulan klien (Section 7), baru klaim final.

## 5. Checklist Audit

### 5a. Rank Math (target skor 80–100 / hijau)
- [ ] Focus keyword di: SEO title, meta description, slug, 10% awal konten, dan ≥2 heading `<h2>`.
- [ ] Paragraf pertama ≥200 kata (override batas 150 kata).
- [ ] Keyword total 31–34× (termasuk di heading), density 1,0–2,5%.
- [ ] Semua occurrence di body text = **Bold + Title Case**; di `<h2>/<h3>` Title Case tanpa `<b>`.
- [ ] Paragraf pertama: permalink format + internal link ke `{client_url}` (anchor `{client_name}`, bold) + ≥1 external link Wikipedia kota (nama kota saja, `target="_blank" rel="noopener noreferrer"`) + focus keyword.
- [ ] `<!--more-->` tepat setelah paragraf pertama.
- [ ] Inbound link (placeholder `<b>INI BAGIAN INBOUND LINK</b>` atau link riil hasil swap) di paragraf 2–5, **setelah** `<!--more-->`.
- [ ] WA shortcode hanya di paling akhir artikel.
- [ ] 1–3 blok gambar (div GAMBAR DISINI / `<img>` riil) dengan alt text mengandung keyword; tidak di tengah paragraf.
- [ ] ≥1 list (`<ul>`/`<ol>`); heading terstruktur untuk TOC; tanpa heading "Kesimpulan".
- [ ] `<p>&nbsp;</p>` sebelum setiap `<h2>` (bukan sebelum `<h3>`); heading tidak dibold.
- [ ] Paragraf ≤150 kata (kecuali paragraf pertama); kalimat rata-rata ≤20–25 kata; transition words; voice aktif dominan.
- [ ] Blok kontak: `<h2>` "Hubungi Kami Dari Kontak Resmi {client_name}" (non-bold) + label WA/Telepon/Email bold.

### 5b. Human-Like (target human score 90%+)
- [ ] Lulus sanity anti-slop: tanpa cliché terlarang, tanpa em dash, tanpa pola kalimat seragam.
- [ ] Sentuhan lokal wajar (nama masakan/kebiasaan daerah) tanpa klaim faktual berlebih.
- [ ] Baca pelan: terdengar seperti orang, bukan model yang mempadding.

### 5c. WordPress + PUEBI + Bahasa Baku
- [ ] Format H2/H3, nbsp, more-tag, shortcode sesuai Section 11.
- [ ] EYD: "silakan", kapital hari/bulan, "di" pisah sebagai kata depan.
- [ ] Semua kata prosa terverifikasi oleh gerbang: kamus `alat/kamus-kata.txt` atau wordlist offline
  `alat/kamus-kbbi-offline.txt`; kata yang dilaporkan tidak terverifikasi ditinjau manual; kata asing
  ditulis ulang sesuai Tahap 3.
- [ ] Format kode aman WordPress: paragraf dipisah baris kosong (wpautop membungkus `<p>`), baris tunggal
  dalam blok kontak menjadi `<br />` (dilakukan WordPress), tanpa komentar blok Gutenberg `<!-- wp:… -->`
  agar wpautop tidak dimatikan (lihat FAKTA-SEO.md bagian WordPress).

## 6. Protokol Crosscheck — ZeroGPT (Tahap 5)

ZeroGPT adalah **satu-satunya** gate detector eksternal. JustDone (AI Detector & Plagiarism) dihapus dari protokol pada 2026-11-20 atas keputusan pemilik project — hasilnya dikunci di balik akun berlangganan sehingga tidak bisa diaudit otomatis.

| Tool | URL | Yang dicek | Target |
|---|---|---|---|
| ZeroGPT | https://www.zerogpt.com/ | % AI (paste teks) | Verdict **"Your Text is Human written"**; AI % serendah mungkin (target praktis di bawah 10%) |

Prosedur:
1. Strip HTML → buang blok editor (saran gambar, shortcode, alt text, baris kontak boilerplate bila perlu) → pastikan payload ≤15.000 karakter (batas gratis ZeroGPT). Artikel ≥2000 kata sering melewati batas ini: bila lebih, pecah di batas paragraf menjadi 2 bagian, uji keduanya, dan laporkan kedua angkanya.
2. Paste ke kolom teks (`#textArea`), klik **"Detect Text"**, tunggu hasil (bisa lebih dari 15 detik; baca ulang sebelum menyimpulkan gagal), lalu rekam angka ke `LAPORAN.md` klien (Section 7).
3. Jika verdict AI: revisi bagian yang ditandai detector → scan ulang (maks 2 iterasi). Laporkan angka apa adanya, jangan manis-maniskan.
4. Bila ZeroGPT mengubah UI atau terhalang captcha: tandai `MANUAL CHECK NEEDED` dan serahkan ke operator — dilarang mengarang angka.
5. Catatan plagiarisme: artikel hasil pipeline ini adalah parafrase utuh (bukan salin-tempel), jadi risiko duplikasi rendah by construction; klaim "lolos plagiarism checker" hanya boleh ditulis bila operator menjalankan cek manual dan melaporkan hasilnya.

## 7. Laporan Per Klien (BUKAN di file ini)

Setiap pekerjaan dilaporkan di `klien/<Klien>/artikel/<YYYY Month>/LAPORAN.md`. AGENT.md tidak pernah diubah untuk mencatat hasil kerja.

`LAPORAN.md` berisi dua bagian. Bagian atas adalah **ledger**, tabel yang dibaca oleh `cek-status.py`. Bagian bawah adalah blok laporan per artikel.

Ledger (satu baris per draft; `-` berarti tahap belum dikerjakan; tanggal `YYYY-MM-DD` berarti sudah):

```
| Draft | Hash | Audit | Humanize | ZeroGPT |
|---|---|---|---|---|
| <nama draft>.txt | <16 karakter hex dari cek-status.py> | 2026-03-01 | 2026-03-01 | 3,72% AI |
```

Aturan ledger: kolom Hash wajib 16 karakter hex agar baris terbaca. Jangan mengubah urutan kolom. Baris ledger tidak pernah dihapus, hanya diperbarui. Format blok laporan (satu blok per artikel, urut tanggal):

```
## <Judul/Slug artikel> — <YYYY-MM-DD>
- File final: <Slug> - Humanized.txt
- Metrik: <kata> kata | paragraf 1: <n> kata | keyword <n>× (density <x>%)
- Temuan audit draft mentah: <daftar FAIL/WARN yang diperbaiki>
- Cek larangan: em dash <n>, cliché <n>, "Anda" salah kapital <n>, staccato <n>
- ZeroGPT: <verdict>, AI <x>% (<n> karakter; bagian 1/2 bila dipecah)
- Plagiarisme: belum dicek manual / <hasil dari operator>
- Catatan/risiko: <hal yang perlu diketahui operator>
```

## 8. Standar Keamanan & Kejujuran Konten

- Tidak ada secret/API key di file project mana pun.
- Angka harga hanya "kisaran"/"tergantung"; tanpa statistik/testimoni/nama/penghargaan fiktif.
- Klaim butuh verifikasi live (harga kompetitor, fakta kota) → tandai eksplisit, jangan mengarang sumber.

## 9. Skill Wajib dan Pustaka SEO (ikut repo, folder `skills/`)

Skill WAJIB dan pustaka SEO opsional keduanya **ikut repo** — tidak diunduh dari luar. Muat dengan
membaca `SKILL.md`-nya (agent dengan mekanisme skill boleh memuatnya lewat mekanisme masing-masing; hasil sama).

### Skill WAJIB

| Tahap | Skill (folder `skills/`) | Peran |
|---|---|---|
| Semua | `dci-seo-auditor` | Skill induk — muat pertama; urutan pipeline, rujukan berkas aturan dan alat |
| 3 — Humanize | `antislop-copywriting` + `antislop` (core) | Filter anti-deteksi inti: 0 em dash, tanpa rule-of-three paksa, tanpa negative parallelism ("bukan hanya X tetapi Y"), tanpa rangkaian fragmen staccato, tanpa fake-candid opener dan buzzword kosong; PERTAHANKAN "signs of human writing" (variasi panjang kalimat, detail spesifik, asides, tension) |
| 5 — Sebelum klaim selesai | `verification-before-completion` | Verifikasi dengan bukti terukur (word count, keyword density, hasil detector) — bukan perasaan |

### Pustaka SEO opsional (ikut repo, pakai sesuai kebutuhan)

Keluarga `blog` lengkap (router + 31 sub-skill) dan 11 skill SEO lain:

| Kelompok | Skill | Kapan dipakai |
|---|---|---|
| Router | `blog` | Melihat seluruh sub-command keluarga blog |
| Perencanaan | `blog-strategy`, `blog-calendar`, `blog-brief`, `blog-cluster` | Strategi per klien, kalender editorial bulanan, brief 1 artikel, cluster hub-and-spoke |
| Menulis | `blog-write`, `blog-outline`, `blog-style` | Draft baru, outline SERP, mempelajari gaya penulis |
| Evaluasi & pemeliharaan | `blog-analyze`, `blog-audit`, `blog-seo-check`, `blog-decay`, `blog-cannibalization` | Skor 100 poin, audit kesehatan, checklist SEO (pembanding gerbang), penurunan GSC, keyword overlap (pembanding cek_lintas) |
| Fakta & riset | `blog-factcheck`, `blog-discourse`, `blog-notebooklm` | Verifikasi statistik ke sumber; riset diskusi 30 hari terakhir; query notebook |
| Teknis & output | `blog-schema`, `blog-chart`, `blog-image`, `blog-repurpose` | JSON-LD, SVG chart, gambar, repurposing lintas kanal |
| Multilingual | `blog-multilingual`, `blog-translate`, `blog-localize`, `blog-locale-audit` | Bila klien minta konten multi-bahasa |
| SEO non-blog | `ai-seo`, `programmatic-seo`, `seo-audit`, `schema`, `site-architecture`, `competitors`, `competitor-profiling`, `content-strategy`, `directory-submissions`, `free-tools`, `marketing-tools`, `aso` | Audit situs klien, halaman skala, schema, arsitektur, kompetitor, backlink direktori |

Catatan `research-guide` adalah skill riset umum di komputer operator (bukan di repo).

Aturan pemakaian:
1. Skill WAJIB tersedia di repo ini (`skills/`) — jangan meminta operator mengunduh, jangan berhenti bila folder hilang; laporkan bahwa repo tidak lengkap.
2. Skill adalah **filter**, bukan pengganti aturan: bila aturan AI Puffer (Section 11) bertentangan dengan preferensi generik skill, **Section 11 menang** (contoh: marker percakapan "jujur saja," memang diwajibkan Section 11; antislop hanya membatasi frekuensinya maks 1–2×).
3. `aturan/kerja-tanpa-skill.md` tetap menjadi inti metode (namanya berarti metode inti yang tidak bergantung skill eksternal) — tetap dibaca sebelum Tahap 3.
4. Skill pustaka SEO bersifat **opsional per kebutuhan** (contoh sah: `blog-factcheck` sebelum publish, `blog-seo-check` ulang setelah revisi detector, `copy-editing` dari komputer operator bila ada permintaan REVISION). Fungsi analisis skrip keluarga blog (`analyze_blog.py` dsb.) berjalan lewat skill ZCode asli bila tersedia; tanpa itu, gunakan gerbang `alat/` sebagai sumber angka.

## 10. Mode Pintasan (input: nama perusahaan + nama bulan)

Operator hanya menyebut **nama perusahaan** dan **nama bulan**. Pemakaian mode ini = izin eksekusi penuh (setara `SKIP PLAN`): kerjakan semua tahap tanpa checkpoint per file, lapor sekali di akhir.

Langkah:
1. **Cari folder klien**: cocokkan nama perusahaan dengan folder di `klien/` (abaikan kapital/spasi; folder berawalan `_` dilewati). Tidak ada atau lebih dari satu kandidat → tanya operator, jangan menebak.
2. **Baca `CLIENT.md`** folder itu untuk mengisi semua `{client_*}`. Tidak ada atau ada field kosong → berhenti dan minta operator melengkapi (jangan mengarang data klien).
3. **Cari folder bulan**: di `klien/<Klien>/artikel/`, ambil folder yang namanya berakhiran nama bulan (mis. "2026 November"). Bila ada beberapa tahun, pakai tahun terbaru dan sebutkan di laporan.
4. **Jalankan Gerbang Status** (Section 4) pada folder bulan itu. Proses hanya draft berstatus `BARU` (audit penuh) dan `LANJUTKAN` (hanya tahap yang masih `-`). `SELESAI`, `MENUNGGU`, `BERUBAH`, `TANPA-CATATAN`, dan `RUSAK` tidak disentuh dan dilaporkan apa adanya. Tidak ada draft yang diproses → lapor, selesai.
5. **Baca `aturan/kerja-tanpa-skill.md`** (skill di Section 9 hanya bila tersedia), lalu per draft jalankan Pipeline Section 4 (audit → humanize → verifikasi script → ZeroGPT Section 6). Draft asli dilarang ditimpa; hasil disimpan sebagai `<nama> - Humanized.txt`.
6. **Tulis laporan** ke `LAPORAN.md` folder bulan itu (format Section 7), bukan ke AGENT.md.
7. **Gerbang kualitas** per artikel sebelum klaim final: `python3 -I -X utf8 alat/cek-artikel.py "<artikel>"`. Perbaiki hanya bagian FAIL (termasuk kata tidak terverifikasi), ulang sampai 0 FAIL.
8. **Laporan akhir ke operator**: tabel status setiap draft (termasuk yang dilewati dan alasannya), tabel ringkas artikel yang diproses (kata, keyword, ZeroGPT), temuan yang butuh keputusan, dan status plagiarisme (belum dicek manual kecuali operator melaporkan).

Cara memanggil: command `/artikel <nama perusahaan> <bulan> [tahun]`, atau prompt biasa untuk agent apa pun. Sumber command ada di `perintah/artikel.md` dan dipasang per komputer dengan `alat/pasang-perintah.py` (TRAE, ZCode, Claude Code). Panduan lengkap, penjelasan isi perintah, dan prompt cadangan ada di `PROMPT PINTASAN.md` (ROOT).

## 11. Template Prompt AI Puffer (aturan konten, GLOBAL)

Ini sumber tunggal aturan konten. Isi placeholder `{client_*}` dari `CLIENT.md` folder klien, `{topic}` dan `{keywords}` dari tugas yang sedang dikerjakan. File `content core ai-puffer.txt` sudah dihapus dan isinya dipindah ke sini apa adanya (satu perubahan: baris sumber data klien kini menunjuk `CLIENT.md`).

```text
Act as a professional SEO Content Writer specialized in {client_niche}. Write a ~2200-word article (minimum 2000 words) in Indonesian about "{topic}", optimized for Rank Math score 80-100 (green). Stay strictly inside the client's business field. DO NOT write about topics outside {client_business}.

===== CLIENT INFORMATION (diisi dari CLIENT.md di folder klien) =====

Client Name: {client_name}
Website: {client_url}
Business: {client_business}
Niche: {client_niche}
WhatsApp shortcode: {client_wa_shortcode}
WA / Telepon: {client_phone}
Email: {client_email}
All internal links and references must point to {client_name} services only. Never mention or link another client.

===== FIRST PARAGRAPH PERMALINK FORMAT =====

- The FIRST paragraph ONLY must start with a permalink format before the content
- Format: <a href="{client_url}/artikel/[judul-atau-subjek-paragraf]"><b><i>[Judul atau Subjek Paragraf]</i></b></a> - [isi paragraf dimulai di sini...]
- The [judul-atau-subjek-paragraf] in URL should be lowercase, hyphenated slug version
- The [Judul atau Subjek Paragraf] as anchor text should be Title Case, bold and italic
- Example: <a href="{client_url}/artikel/keunggulan-layanan"><b><i>Keunggulan Layanan</i></b></a> - Dalam setiap penyelenggaraan kegiatan, ...
- After the first paragraph, continue with normal paragraphs WITHOUT permalink format

===== INBOUND LINK PLACEHOLDER RULES =====

- MUST include 1 inbound link placeholder in paragraphs 2-5 (early in the article, after <!--more-->)
- Format: <b>INI BAGIAN INBOUND LINK</b>
- The placeholder text MUST be contextually relevant and blend naturally with the paragraph topic
- Write the placeholder as part of a sentence that connects to the article discussion
- The text should appear as a natural continuation of the paragraph, NOT forced or obvious
- Example integration: "Nah, untuk kebutuhan di wilayah lain, anda bisa cek <b>INI BAGIAN INBOUND LINK</b> yang juga menawarkan variasi layanan lengkap dengan harga terjangkau."
- Alternative example: "Selain itu, <b>INI BAGIAN INBOUND LINK</b> dapat menjadi pilihan alternatif untuk kebutuhan anda."
- Place this placeholder naturally within the content flow in one of paragraphs 2-5
- Place the WhatsApp shortcode {client_wa_shortcode} ONLY at the very end of the article, after the final paragraph

===== RANK MATH SEO RULES =====

- Don't write title in content area, just skip into first paragraph
- "{keywords}" MUST appear in: SEO title, meta description, slug, first 10% of content (~200 words), and at least TWO <h2> subheadings. The FIRST paragraph must be at least 200 words (this specific rule overrides the general 150-word paragraph cap below).
- Keyword density: repeat "{keywords}" 31-34 times naturally, density 1.0%-2.5% (occurrences / total words, as Rank Math counts it). Every occurrence in body text MUST be Bold and Title Case (e.g., <b>Jasa Catering Blitar</b>). Occurrences inside <h2>/<h3> stay Title Case but NOT wrapped in <b> (headings are never bold) and still count toward the total.
- Internal link: in first paragraph, put link to "{client_url}" with anchor text {client_name} (bold).

for example the code used should be look like this,
<a class="ng-star-inserted" href="{client_url}" target="_blank" rel="noopener" data-hveid="0" data-ved="0CAAQ_4QMahgKEwi4j9-olc6SAxUAAAAAHQAAAAAQuQE"><b>{client_name}</b></a>

- External link: at least 1 link for the city/region in topic (add target="_blank" rel="noopener noreferrer"). for example you can take from wikipedia source of the city/region (e.g. "Blitar"). but the hyperlinked text only on the city/region name, don't put it on "from wikipedia source of ..." instead only put on the name itself (e.g. "Blitar")

for example the code used should be look like this,
<a class="ng-star-inserted" href="https://id.wikipedia.org/wiki/Kota_Blitar" target="_blank" rel="noopener noreferrer" data-hveid="0" data-ved="0CAAQ_4QMahgKEwi4j9-olc6SAxUAAAAAHQAAAAAQtwE">Blitar</a>

- Include 1-2 image alt text suggestions containing keyword: <!-- Suggested Image: [desc] | Alt text: "{keywords} - [desc]" -->
- Structure headings clearly for Rank Math TOC auto-generation.
- Readability: short paragraphs (max 150 words, except the first paragraph), avg sentence ≤20-25 words, active voice preferred, frequent transition words ("selain itu,", "di sisi lain,", "menariknya,", "oleh sebab itu,", etc.), include at least 1 list (<ul> or <ol>).

===== HUMAN-LIKE WRITING (MUST pass AI detectors such as ZeroGPT, human score 90%+) =====

- Vary sentence length: short (5-8 words), medium (12-18), occasional long (20-30). NO uniform-length patterns.
- Conversational tone: use "nah,", "jujur saja,", "sebenarnya,", "kalau menurut pengalaman,", "percaya atau tidak,". Address reader directly: "anda pasti pernah...", "coba bayangkan...", "mungkin anda bertanya-tanya...". Each of these openers max 1-2x per article so they do not become a pattern.
- Human quirks: rhetorical questions ("Lalu, bagaimana solusinya?"), filler phrases ("yang jelas,", "pada kenyataannya,", "satu hal yang perlu diingat,"), idiomatic expressions ("tidak ada salahnya", "jangan sampai", "sudah bukan rahasia lagi").
- Anti-AI patterns: NO consecutive paragraphs starting with same word. NO repetitive formal phrases ("Dalam hal ini,", "Oleh karena itu,"). NO predictable list patterns. Vary paragraph lengths (2-7 sentences). NO em dash. NO forced rule-of-three, NO "bukan hanya X, tetapi Y" formula, NO staccato fragment runs.
- Add storytelling & realistic details: scenarios, approximate costs, timeframes, common challenges in the client's field. Costs are only ranges labeled "kisaran"/"tergantung"; never invent statistics, testimonials, client names, awards, or years of experience.
- Burstiness: alternate dense detail sections with casual/opinion paragraphs.
- Natural keyword integration — weave, don't force. Occasionally paraphrase around the keyword.
FORBIDDEN cliché phrases: "Di era modern ini", "Dalam dunia yang semakin berkembang", "Tidak dapat dipungkiri", "Perlu diketahui bahwa", "Sangat penting untuk", "Merupakan salah satu", "Berbagai macam", "Memainkan peran penting". Use fresh expressions instead.

===== "ANDA" CAPITALIZATION =====

- Capital "Anda" ONLY at sentence start (after . ? ! or first word of paragraph).
- All other positions: lowercase "anda".
- ✅ "Jika anda membutuhkan..." | ✅ "Anda bisa menghubungi..." | ❌ "Jika Anda membutuhkan..."

===== WORDPRESS FORMATTING =====

- First paragraph: permalink format + internal link ({client_name}) + Wikipedia external link + focus keyword.
- <!--more--> tag: immediately after first paragraph.
- Make the "Hubungi Kami Dari..." as <h2> not bold, and keep the others just like the same with format like bold below.

Hubungi Kami Dari Kontak Resmi {client_name}
<b>WA:</b> {client_phone}
<b>Telepon:</b> {client_phone}
<b>Email:</b> {client_email}

- Headings: <h2> for subheadings, <h3> for sub-points. Do NOT bold headings.
- <p>&nbsp;</p> ONLY before every <h2> tag (NOT before <h3>).
- NO "Kesimpulan"/"Conclusion" header — end naturally.
- PUEBI standard Indonesian spelling (e.g. "silakan" bukan "silahkan"; nama hari dan bulan diawali huruf kapital).

===== IMAGE PLACEHOLDERS (1-3 blocks, placed naturally — NOT mid-paragraph) =====
Recommended positions: after <!--more-->/shortcode, after storytelling paragraphs, near lists, between major sections, before closing.

Format:

<div style="border: 2px dashed #ff6600; padding: 15px; margin: 20px 0; text-align: center; background-color: #fff8f0;">
<strong>GAMBAR DISINI</strong><br> <em>Saran: [deskripsi kontekstual]
</em><br> <small>Alt text: "{keywords} - [deskripsi singkat]"</small>
</div>

===== ARTICLE STRUCTURE =====

<p><a href="{client_url}/artikel/[slug]"><b><i>[Title]</i></b></a> - [Opening paragraph ≥200 words: link {client_name} + Wikipedia + keyword]</p>
<!--more-->
[📷 GAMBAR DISINI]
<p>&nbsp;</p>
<h2>[Subheading]</h2>
<p>Content...</p>
[📷 GAMBAR DISINI]
<p>&nbsp;</p>
<h2>[Subheading with {keywords}]</h2>
<ul/ol>List...</ul/ol>
... (continue with natural variation) ...
<p>&nbsp;</p>
<h2>Hubungi Kami Dari Kontak Resmi {client_name}</h2>
[contact block]
[📷 GAMBAR DISINI]
<p>[Final paragraph — warm, natural close]</p>
{client_wa_shortcode}

Topic: "{topic}"
Keywords: "{keywords}"
```
