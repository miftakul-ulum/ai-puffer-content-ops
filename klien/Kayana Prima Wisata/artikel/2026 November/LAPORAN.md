# Laporan Artikel Kayana Prima Wisata, November 2026

> LAPORAN pengganti. LAPORAN sebelumnya beserta berkas Humanized lama dihapus sengaja oleh Mas Ulum (2026-11-20, belum masuk git) dan hasil audit lamanya dinyatakan dilupakan. Keempat artikel dikerjakan ulang dari nol dari draft mentah yang sama pada 2026-11-20; hash di bawah disalin dari keluaran `alat/cek-status.py` pada draft yang tidak berubah.

| Draft | Hash | Audit | Humanize | ZeroGPT |
|---|---|---|---|---|
| Booking Sewa Mobil Malang.txt | d26a653598561183 | 2026-11-20 | 2026-11-20 | Bagian 1: 6,6% AI; bagian 2: 0% AI |
| Sewa Mobil Malang Perjalanan Bisnis.txt | 1641d9350fc1c507 | 2026-11-20 | 2026-11-20 | Bagian 1: 16,43% AI; bagian 2: 0% AI |
| Sewa Mobil Malang Plus Sopir.txt | 44139068b07f93ba | 2026-11-20 | 2026-11-20 | 21,3% AI |
| Sewa Mobil Malang Tour Keluarga.txt | 45a031d5511fa044 | 2026-11-20 | 2026-11-20 | - |

## Catatan konteks, 2026-11-20
- Kelima berkas keluaran lama (4 Humanized + LAPORAN.md) dihapus Mas Ulum dari working tree tanpa commit, lalu dinyatakan dilupakan. Draft mentah tidak pernah berubah (hash sama dengan ledger lama di HEAD git). Semua hasil di dokumen ini adalah kerja ulang penuh dari draft mentah, bukan pemulihan berkas lama.
- Tiga draft berstatus MENUNGGU menurut gerbang karena klien ini tidak memiliki shortcode WA (field `{client_wa_shortcode}` kosong di CLIENT.md). Keempatnya tetap dikerjakan mengikuti instruksi kerja ulang Mas Ulum dan pengecualian klien tanpa WA yang sudah tercatat sebelumnya. Artikel Humanized ditutup blok kontak + paragraf penutup tanpa shortcode.
- Verifikasi live situs klien gagal pada sesi ini: `https://www.kayanaprimawisata.co.id` tidak dapat dibuka (WebFetch gagal dua kali) dan `https://www.kayanaprimawisata.co.id/layanan-kami/` mengembalikan HTTP 404. Konsekuensinya: alamat kantor, jam operasional, dan semua angka tarif dari draft tidak dipertahankan (status `TIDAK TERVERIFIKASI`, tidak bisa dibuka). Jenis armada (mobil keluarga, Elf, Hiace, bus pariwisata) dibawa dari draft dan istilah CLIENT.md, ditulis sebagai poin diskusi, bukan klaim stok. Destinasi dari draft (Jatim Park, Museum Angkut, Coban Rondo, Alun-Alun Kota Malang) dipertahankan dengan pengaman eksplisit: cek jam operasional, harga tiket, dan ketentuan lewat kanal resmi destinasi.
- Harga tidak ditulis dalam bentuk nominal apa pun; semua pembahasan biaya bersifat faktor kualitatif + kewajiban minta penawaran tertulis.
- Gerbang kualitas terakhir (berkas terbaru, 2026-11-20): keempat artikel `0 FAIL`. WARN sisa adalah kata belum terverifikasi wordlist offline (antar-, elf, pertimbangkan, kayanaprimawisata, co, dan sejenisnya) — ditinjau manual dan dinyatakan wajar: "elf" adalah istilah armada bawaan draft/klien, sisanya bentukan tata bahasa dan nama domain.
- Cek kanibalisasi antarartikel sempat FAIL pada Plus Sopir vs Tour Keluarga (2 kalimat identik 8+ kata: "Mungkin anda bertanya-tanya, berapa banyak tempat yang realistis dikunjungi…" dan "Hiace maupun Elf menuntut anggaran lebih besar, belum lagi bus untuk rombongan besar"). Sudah diperbaiki dengan mengubah sudut kalimat di Tour Keluarga, dan gerbang final keempat artikel menunjukkan 0 FAIL.

## Booking Sewa Mobil Malang — 2026-11-20
- File final: `Booking Sewa Mobil Malang - Humanized.txt`
- Metrik: 2.074 kata | paragraf 1: 206 kata | keyword 32x (density 1,54%) | 4 heading H2 berkeyword
- Gerbang terakhir: 0 FAIL, 8 WARN, 3 INFO.
- Temuan audit draft mentah yang ditangani: 16 temuan (kata asing "booking" di luar keyword, 8 em/en dash, 4 kutip miring, angka tarif tanpa label, rule-of-three 30x, format `<strong>`/`<em>` yang tidak terbaca gerbang sebagai `<b>`, tanpa more-tag, nbsp tanpa `<p>`, heading kontak tidak baku, anchor permalink). Ditambah: nominal harga dihapus sepenuhnya (tidak terverifikasi), blok kontak baku + 3 blok gambar template + placeholder inbound link ditambahkan.
- Cek larangan: em/en dash 0; kutip miring 0; "Anda" salah kapital 0; rule-of-three pola "A, B, dan C" dihindari saat penulisan.
- ZeroGPT (2026-11-21): bagian 1 (14.621 karakter) "Your Text is Human written", 6,6% AI; bagian 2 (682 karakter) "Your Text is Human written", 0% AI. Keduanya di bawah target praktis 10%.
- Plagiarisme: belum dicek manual; artikel adalah parafrase ulang penuh sehingga risikonya rendah by construction, tapi klaim lolos plagiarisme hanya boleh ditulis bila operator menjalankan cek manual.
- Catatan/risiko: `INI BAGIAN INBOUND LINK` perlu diganti tautan riil sebelum terbit; dua blok gambar + satu blok penutup perlu foto asli dengan alt sesuai; skor Rank Math aktual di WordPress belum diukur; situs klien tidak bisa dibuka saat sesi ini sehingga tidak ada klaim terverifikasi tambahan.

## Sewa Mobil Malang Perjalanan Bisnis — 2026-11-20
- File final: `Sewa Mobil Malang Perjalanan Bisnis - Humanized.txt`
- Metrik: 2.044 kata | paragraf 1: 209 kata | keyword 33x (density 1,61%) | 4 heading H2 berkeyword
- Gerbang terakhir: 0 FAIL, 10 WARN, 3 INFO.
- Temuan audit draft mentah yang ditangani: 10 temuan tanpa keyword + 27 dengan `--kw` (1.678 kata <2000, P1 0 kata, keyword 19x tidak dibold, tanpa blok gambar, heading kontak `<h3>` tidak baku, 5 em/en dash, "Anda" kapital tengah kalimat, ritme paragraf seragam 38/47, kalimat pendek 9%, rule-of-three 21x). Draft juga memuat tautan riil "Pusat Sewa Mobil Malang Semua Armada" yang keberadaannya tidak terverifikasi → diganti placeholder `<b>INI BAGIAN INBOUND LINK</b>`. Alamat kantor dan jam operasional pada blok kontak draft tidak dipertahankan (tidak terverifikasi).
- Cek larangan: em/en dash 0; kutip miring 0; "Anda" salah kapital 0; rule-of-three dihindari saat penulisan; nominal harga tidak ditulis.
- ZeroGPT (2026-11-21): bagian 1 (14.688 karakter) "Your Text is Most Likely Human written, may include parts generated by AI/GPT", 16,43% AI; bagian 2 (328 karakter) "Your Text is Human written", 0% AI. Bagian 1 di atas target praktis 10% — diputuskan TIDAK direvisi buta karena kuota deteksi sesi habis sehingga revisi tidak bisa diverifikasi ulang hari ini; angka dicatat apa adanya dan perlu keputusan operator (revisi terarah + scan ulang setelah kuota reset, mengikuti protokol maks 2 iterasi).
- Plagiarisme: belum dicek manual.
- Catatan/risiko: placeholder inbound link perlu diganti tautan riil; foto blok gambar belum diisi; skor Rank Math aktual belum diukur.

## Sewa Mobil Malang Plus Sopir — 2026-11-20
- File final: `Sewa Mobil Malang Plus Sopir - Humanized.txt`
- Metrik: 2.018 kata | paragraf 1: 217 kata | keyword 32x (density 1,59%) | 4 heading H2 berkeyword
- Gerbang terakhir: 0 FAIL, 7 WARN, 3 INFO.
- Temuan audit draft mentah yang ditangani: 12 temuan (em/en dash, 6 kutip miring, angka "sekitar Rp500.000-Rp900.000" tanpa label → nominal dihapus, ritme seragam 36/56, rule-of-three 17x, anchor permalink "Perjalanan Nyaman Di Malang" yang salah kapital "di" → diganti anchor keyword baku). Istilah MPV dari draft ditulis ulang menjadi "mobil keluarga" agar tidak masuk kata asing.
- Cek larangan: em/en dash 0; kutip miring 0; "Anda" salah kapital 0; nominal harga tidak ditulis.
- ZeroGPT (2026-11-21): satu bagian (14.662 karakter, artikel utuh di bawah 15.000) "Your Text is Likely Human written, may include parts generated by AI/GPT", 21,3% AI. Di atas target praktis 10%; perlakuan sama dengan Perjalanan Bisnis: dicatat apa adanya, revisi ditunda sampai bisa diverifikasi ulang (kuota deteksi sesi habis), keputusan di operator.
- Plagiarisme: belum dicek manual.
- Catatan/risiko: placeholder inbound link + foto blok gambar perlu ditindaklanjuti; skor Rank Math aktual belum diukur.

## Sewa Mobil Malang Tour Keluarga — 2026-11-20
- File final: `Sewa Mobil Malang Tour Keluarga - Humanized.txt`
- Metrik: 2.020 kata | paragraf 1: 210 kata | keyword 32x (density 1,58%) | 5 heading H2 berkeyword
- Gerbang terakhir: 0 FAIL, 8 WARN, 3 INFO.
- Temuan audit draft mentah yang ditangani: 19 temuan (11 em/en dash, 4 kutip miring, anggaran contoh "Rp3.000.000" tanpa label → contoh nominal dihapus menjadi pembagian pos kualitatif, ritme seragam 20/49, rule-of-three 18x, meta SEO tertanam di ekor draft dipindah ke berkas `- Meta.txt`, anchor permalink "Liburan Keluarga Di Malang" → diganti anchor keyword). Kalimat-kalimat identik dengan Plus Sopir ditemukan gerbang dan ditulis ulang (lihat catatan konteks).
- Cek larangan: em/en dash 0; kutip miring 0; "Anda" salah kapital 0; nominal harga tidak ditulis.
- ZeroGPT: MANUAL CHECK NEEDED (2026-11-21). Enam pemeriksaan pertama di sesi browser sukses, setelah itu tombol Detect Text tidak lagi menghasilkan keluaran pada halaman baru maupun setelah reload (diduga kuota deteksi gratis sesi/IP habis; tidak ada captcha maupun pesan galat yang tampil). Payload siap di `Temp/dci-payloads/payload-tourkeluarga-bagian1.txt` (14.482 karakter) dan `bagian2.txt` (469 karakter); silakan ditempel manual ke zerogpt.com setelah kuota reset, atau minta agent mengulang di sesi baru. Dilarang mencatat angka tanpa pemindaian nyata.
- Plagiarisme: belum dicek manual.
- Catatan/risiko: placeholder inbound link + foto blok gambar perlu ditindaklanjuti; skor Rank Math aktual belum diukur; destinasi dari draft (Jatim Park, Museum Angkut, Coban Rondo) tetap perlu verifikasi jam/tiket lewat kanal resmi sebelum tayang.

## Ringkasan status keputusan operator
1. Perjalanan Bisnis (16,43%) dan Plus Sopir (21,3%): revisi terarah + scan ulang (maks 2 iterasi) atau terima angka — menunggu keputusan.
2. Tour Keluarga: dua bagian menunggu pemeriksaan manual/ulang ZeroGPT.
3. Placeholder `INI BAGIAN INBOUND LINK` di keempat artikel masih menunggu tautan riil hasil swap.
4. Blok gambar di keempat artikel masih saran; foto asli + alt sesuai keyword perlu diisi.
5. Rank Math aktual di WordPress belum diukur; plagiarisme belum dicek manual.
6. Situs klien tidak bisa dibuka pada sesi ini; alamat/jam operasional/tarif tetap tidak dipromosikan sampai terverifikasi.

Copyright © 2026 Duta Corpora Indonesia — All rights reserved
