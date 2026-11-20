# Aturan Kerja Mandiri

> Author: Mas Wondho — Duta Corpora Indonesia (DCI)
> Copyright © 2026 Duta Corpora Indonesia — All rights reserved

Berkas ini berdiri sendiri. Karyawan tidak perlu memasang skill apa pun, dan agent apa pun yang bisa membaca berkas biasa (TRAE, ZCode, Claude Code, Codex, dan lainnya) bisa memakainya. Skill yang ada di komputer pemilik project bersifat opsional (lihat bagian 8). Bila ada pertentangan, urutan menangnya: `AGENT.md` Section 11, lalu berkas ini, lalu skill apa pun.

## 1. Metode menulis ulang (Tahap 3)

1. Baca draft dan daftar TEMUAN dari `--draft` tanpa mengubah apa pun.
2. Catat suara penulis aslinya: panjang kalimat, cara menyapa pembaca, istilah khas. Pertahankan, jangan diseragamkan.
3. Tulis ulang paragraf demi paragraf. Mengganti beberapa kata saja tidak cukup.
4. Jangan menambah fakta yang tidak ada di draft atau di situs klien.
5. Jalankan gerbang kualitas, lalu perbaiki hanya baris yang FAIL. Jangan menulis ulang seluruh artikel.

## 2. Tanda tulisan mesin dan perbaikannya

| Tanda | Contoh | Perbaikan |
|---|---|---|
| Kata sifat kosong tanpa bukti | "solusi terbaik", "berkualitas tinggi", "profesional dan terpercaya" | Sebut hal konkret yang ada di situs klien: menu, jadwal, wilayah layanan |
| Pembuka basa-basi | "Tahukah anda bahwa...", "Di era modern ini" | Mulai dari situasi pembaca atau langsung ke pokok |
| Penutup motivasi | "Jadi, tunggu apa lagi?" | Tutup dengan fakta atau ajakan yang spesifik, misalnya cara memesan |
| Tiga serangkai dipaksakan | "cepat, mudah, dan terjangkau" di setiap bagian | Pakai jumlah butir yang memang dibutuhkan isi |
| Rumus "bukan hanya X, tetapi juga Y" | Diulang di beberapa paragraf | Nyatakan langsung apa yang ditawarkan |
| Kalimat pasif tanpa pelaku | "Pesanan akan diproses" | "Tim dapur memproses pesanan" |
| Sinonim bergantian demi variasi | "layanan", "jasa", "servis", "pelayanan" untuk hal yang sama | Ulangi kata yang paling jelas |
| Tebal, huruf besar, dan tanda kutip berlebihan | Banyak kata ditebalkan di luar keyword | Tebal hanya untuk keyword sesuai aturan template |
| Janji tanpa bukti | "harga termurah", "terbaik di Blitar" | Hapus, atau ganti dengan fakta yang bisa dicek |

Jangan sampai terlalu steril. Tulisan tanpa suara sama mudah dikenali sebagai buatan mesin. Sisakan detail yang spesifik, kalimat pendek sesekali, dan selingan seperlunya.

## 3. Fakta dan klaim

- Klaim berarti angka, harga, nama menu, kebiasaan suatu kota, nama orang atau lembaga, dan peringkat.
- Setiap klaim harus punya sumber yang benar-benar dibuka pada sesi ini (situs klien atau halaman referensi). Tidak ada sumber, klaimnya dihapus.
- Catat klaim penting di `LAPORAN.md` dengan status `TERVERIFIKASI` (alamat sumber, tanggal akses, kutipan paling banyak 25 kata) atau `TIDAK TERVERIFIKASI`. Yang kedua tidak boleh tayang.
- Mencocokkan klaim dengan sumber hanya membuktikan sumber itu memang menyebutnya. Itu belum membuktikan sumbernya benar.
- Ringkasan otomatis dari alat pembaca halaman bukan bukti. Angka atau kalimat yang dipakai harus tampak di teks yang dikembalikan.
- Bila alat pembaca halaman tidak tersedia, tulis `TIDAK TERVERIFIKASI (tidak bisa dibuka)`. Jangan mengisi dari ingatan.

## 4. Sebelum menyatakan selesai

1. Tentukan perintah yang membuktikan klaim.
2. Jalankan perintah itu sekarang, bukan mengandalkan hasil lama.
3. Baca seluruh keluaran dan periksa kode keluarnya.
4. Nyatakan hasilnya apa adanya, lengkap dengan angkanya.

Kata "lulus" hanya boleh dipakai bila gerbang kualitas terbaru, pada berkas terbaru, menunjukkan `0 FAIL`. Setiap kali artikel diedit, gerbang dijalankan ulang. Angka ZeroGPT hanya boleh berasal dari hasil pemindaian nyata. Kalimat seperti "seharusnya lolos" tidak diterima.

## 5. Judul SEO, deskripsi meta, dan slug

Ketiganya tidak ada di badan artikel, jadi disimpan di berkas pendamping `<nama artikel> - Meta.txt`, di folder yang sama dengan artikel. Nama dasarnya sama dengan artikel tanpa ` - Humanized`. Isinya tiga baris:

```text
Judul SEO: <teks>
Deskripsi meta: <teks>
Slug: <teks>
```

Gerbang kualitas memeriksa:
- Judul SEO memuat fokus keyword. Panjang di atas sekitar 60 karakter diberi peringatan.
- Deskripsi meta memuat fokus keyword. Sebaiknya keyword muncul di 160 karakter pertama. Google memotong sesuai lebar perangkat, jadi panjang bukan batas keras.
- Slug memakai huruf kecil, angka, dan tanda hubung, memuat keyword, dan sama dengan slug pada tautan permalink di paragraf pertama.
- Klaim superlatif seperti "termurah" atau "terbaik" diberi peringatan. Pastikan terbukti, atau ganti.

Berkas ` - Meta.txt` bukan draft. Gerbang status melewatinya, dan berkas ini tidak masuk ledger.

## 6. Kanibalisasi dan salinan antar artikel

Gerbang kualitas membandingkan artikel dengan artikel final lain di `klien/`:
- Keyword sama dengan artikel lain milik klien yang sama: FAIL (dua halaman berebut kata yang sama).
- Keyword mirip: peringatan. Pastikan maksud pencariannya berbeda.
- Tiga rangkaian delapan kata atau lebih yang sama dengan artikel mana pun, termasuk milik klien lain: FAIL.

Cara memperbaiki bukan mengganti sinonim, melainkan mengubah sudut pandang: siapa pembacanya, kebutuhan apa, dan keputusan apa yang sedang ia ambil. Dua klien dengan keyword serupa di kota berbeda boleh sama topiknya, tetapi tidak boleh sama kalimatnya.

## 7. Urutan kerja ringkas

1. Gerbang status, lalu audit `--draft`.
2. Tulis ulang sesuai bagian 1 dan 2, periksa fakta sesuai bagian 3.
3. Tulis berkas `- Meta.txt` sesuai bagian 5.
4. Gerbang kualitas sampai `0 FAIL`, lalu ZeroGPT dipindai operator.
5. Catat ledger dan laporan. Sebelum menyatakan selesai, ikuti bagian 4.

## 8. Skill opsional

Bila agent memilikinya, skill berikut boleh dipakai sebagai pelengkap. Tidak ada yang wajib, dan isinya tidak disalin ke repo ini.

| Skill | Gunanya | Catatan lisensi |
|---|---|---|
| `blog-seo-check` | Validasi on-page tambahan | MIT (tercantum di berkas skill). Bergantung pada folder `blog` di sebelahnya, tidak bisa berdiri sendiri |
| `blog-rewrite` | Metode menulis ulang | MIT (tercantum). Sama, bergantung pada folder `blog` |
| `blog-factcheck` | Memeriksa sumber yang dikutip | MIT (tercantum) |
| `antislop-copywriting` | Katalog pola tulisan mesin yang lebih lengkap | Bagian dari antislop, MIT menurut halaman repo `miqdadbadjuber/anti-slop` (dicek 2026-11-20) |
| `verification-before-completion` | Disiplin bukti sebelum klaim selesai | Asal pastinya belum terverifikasi. Plugin `superpowers` memuat skill bernama sama dengan lisensi MIT, tetapi salinan lokal berbeda isinya |
