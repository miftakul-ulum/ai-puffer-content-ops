# LAPORAN — Salimah Catering, 2026 November

> Format mengikuti `AGENT.md` Section 7. Laporan klien ini hanya ditulis di sini, bukan di AGENT.md.

## Ledger (dibaca oleh `alat/cek-status.py`, jangan ubah urutan kolom)

| Draft | Hash | Audit | Humanize | ZeroGPT |
|---|---|---|---|---|
| Jasa Catering Instansi Blitar.txt | 474359ae808f44fb | 2026-11-20 | 2026-11-20 | 3,7% AI (versi final, putaran 2) |

## Laporan per artikel

## Jasa Catering Instansi Blitar — 2026-11-20
- File final: `Jasa Catering Instansi Blitar - Humanized.txt` (draft asli tidak ditimpa)
- Metrik (putaran 1, sudah diganti): 2.098 kata | paragraf 1: 206 kata | keyword 33× di teks, 35 dengan 2 alt text (density ±1,6%). Angka final setelah Putaran 2: 2.073 kata, paragraf 1: 202 kata, keyword 31×, density ±1,50%.
- Temuan audit draft mentah yang diperbaiki:
  - Paragraf 1 hanya ±70 kata (rule ≥200)
  - Inbound link berada sebelum `<!--more-->` (rule: setelahnya)
  - Keyword ±18× (rule 31–34)
  - "silahkan" (PUEBI: "silakan")
  - `&nbsp;` tanpa `<p></p>` sebelum H2
  - Tidak ada blok saran gambar dengan alt text keyword
  - Ritme kalimat dan paragraf seragam
- Perbaikan tambahan saat crosscheck: pola "A, B, dan C" 18 menjadi 8, tiga kalimat pendek berurutan digabung, `&nbsp;` ganda di sekitar gambar dirapikan, nama hari dikapitalkan, satu paragraf yang mengulang isi paragraf lain diganti
- Cek larangan: em dash 0, cliché 0, "Anda" salah kapital 0, staccato 0 (satu-satunya kecocokan adalah blok kontak WA/Telepon/Email, bukan prosa)
- ZeroGPT: "Your Text is Human written", AI 3,72% (14.693 karakter prosa, satu bagian)
- Plagiarisme: belum dicek manual
- Catatan/risiko:
  - Dua kalimat tetap di atas 30 kata (31 dan 32 kata). Satu kalimat 37 kata memuat dua anchor link, dibiarkan agar tautan tidak terganggu.
  - Inbound link di draft asli sudah berupa link riil ke `jasa-catering-kantor-blitar` (bukan placeholder), dan posisinya saya pindah ke setelah `<!--more-->`. Pastikan URL itu benar-benar terbit di situs klien.

## Putaran 2 — fakta, bahasa, dan format WordPress (2026-11-20)

Riset langsung ke dokumen resmi (detail dan tanggalnya ada di `FAKTA-SEO.md`). Perubahan pada artikel:

- **Kata asing ditulis ulang ke padanan KBBI**: nasi box → nasi kotak, snack box → kotak kudapan,
  dessert → pencuci mulut, coffee break → rehat kopi, partner → mitra, capcay → capcai, plus → ditambah,
  familiar → "sudah akrab di lidah". Fokus keyword, nama brand, label kontak, dan shortcode dipertahankan.
- **Fakta ditarik/pinkan yang tidak bersumber**: kisaran harga rupiah (situs klien tidak memuat harga),
  "sambal korek" sebagai selera Blitar (khas Surakarta, bukan Blitar), "cukup banyak kantor pemerintahan
  dan sekolah" (Wikipedia tidak mendukung jumlahnya), ambang "lima puluh orang" dan "peserta ratusan".
  Diganti pernyataan hati-hati; pecel Blitar dipertahankan (varian pecel Blitar terdokumentasi di Wikipedia).
- **Heading**: 2 dari 7 h2 yang semula mengawali fokus keyword diubah agar pola tidak berulang; kini 3 h2
  memuat keyword (minimal aturan: 2). Hirarki h2→h3 diperiksa, tidak ada lompatan.
- **Alt text gambar terpasang** menjadi deskriptif sesuai Google Images (keyword + deskripsi isi foto);
  posisi gambar, ukuran, dan shortcode tidak disentuh.
- **Keyword density** diturunkan ke 31×/2.073 kata = ±1,50% (band skor penuh Rank Math 1–1,5%;
  Google tidak menetapkan angka).

Hasil pemeriksaan:
- Gerbang `alat/cek-artikel.py`: 0 FAIL, 0 WARN (2.073 kata; P1 202 kata; keyword 31×; h2 berkeyword 3;
  format WordPress lolos uji render `wpautop` asli — more-tag, nbsp, gambar, blok kontak, shortcode utuh).
- ZeroGPT versi final: **"Your Text is Human written", AI 3,7%** (14.764 karakter prosa).

Hal yang perlu keputusan/perhatian operator:
1. Halaman live `artikel/jasa-catering-instansi-blitar/` masih menampilkan **draf mentah**; versi Humanized belum dipasang.
2. Meta description di halaman live menjanjikan "harga termurah" dan menyebut "syukuran" — klaim tak terverifikasi dan di luar topik instansi. Usulan pengganti (untuk Rank Math): title `Jasa Catering Instansi Blitar | Salimah Catering`; description `Jasa catering instansi Blitar untuk rapat, bimtek, dan kegiatan dinas: nasi kotak, kotak kudapan, prasmanan, dan katering harian dari Salimah Catering.` (215 karakter, keyword di awal; Google tidak menetapkan batas panjang, snippet dipotong sesuai lebar perangkat).
3. `0812-9278-9024` muncul hanya di tag `<title>` beranda sebagai bagian dari judul SEO; nomor yang dipakai sebagai kontak di beranda (3×), halaman layanan, footer, dan artikel adalah `0857-3627-0963` (sama dengan CLIENT.md). Jadi ini inkonsistensi judul halaman, bukan dua nomor kontak yang bersaing. Bila ingin rapi, judul SEO beranda sebaiknya diselaraskan dengan nomor kontak resmi.
4. Verifikasi KBBI massal tertunda: kuota pencarian harian tanpa akun terpakai saat riset. Jalankan `--kbbi --simpan-kata` di lain hari untuk verifikasi penuh; untuk sementara kamus memuat hasil tinjauan manual seluruh kata artikel.
5. Kisaran harga nasi box ("belasan ribu" dan "tiga puluhan ribu") adalah perkiraan umum berlabel kisaran, bukan daftar harga Salimah. Sesuaikan bila klien punya harga resmi.
