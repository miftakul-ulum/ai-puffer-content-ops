Kerjakan artikel SEO satu klien untuk satu bulan dengan DCI SEO Auditor.

Argumen dari operator: {{ARGUMEN}}

Cara membaca argumen:
- Kata terakhir adalah nama bulan. Bila kata terakhir berupa angka 4 digit, itu tahun dan nama bulan adalah kata sebelumnya.
- Semua kata di depannya adalah nama perusahaan (boleh lebih dari satu kata).
- Argumen kosong atau tidak bisa dibaca: tanyakan ke operator, jangan menebak.
- Contoh: `Salimah Catering November` berarti klien "Salimah Catering", bulan "November". `Salimah Catering November 2026` menambahkan tahun.

Lokasi project: folder yang memuat `AGENT.md` dan `alat/` (root repo). Jalankan semua perintah dari folder itu. Bila agent tidak berada di sana, pindah dulu atau minta operator membuka folder yang benar.

Skill WAJIB dan sudah disediakan di repo: baca `skills/dci-seo-auditor/SKILL.md` sebagai langkah pertama, lalu muat `skills/antislop-copywriting/SKILL.md`, `skills/antislop/SKILL.md`, dan `skills/verification-before-completion/SKILL.md` (baca berkas SKILL.md-nya langsung; tidak perlu mekanisme skill khusus agent). Jangan mengunduh skill lain dari luar repo.

Langkah kerja:
1. Baca `AGENT.md` dan `aturan/kerja-tanpa-skill.md`.
2. Ikuti `AGENT.md` Section 10 (Mode Pintasan) sampai selesai. Pipeline ada di Section 4, checklist di Section 5, ZeroGPT di Section 6, format laporan di Section 7, aturan konten lengkap di Section 11.
3. Sebelum audit apa pun, jalankan Gerbang Status: `{{PYTHON}} -I alat/cek-status.py "klien/<Klien>/artikel/<YYYY Bulan>"`. Proses hanya draft `BARU` dan `LANJUTKAN`. Draft `SELESAI`, `MENUNGGU`, `BERUBAH`, `TANPA-CATATAN`, dan `RUSAK` tidak boleh disentuh.
4. Audit draft mentah dengan `{{PYTHON}} -I -X utf8 alat/cek-artikel.py "<draft>" --draft`. Daftar TEMUAN-nya menjadi bahan humanize.
5. Setelah humanize, tulis berkas `<artikel> - Meta.txt` (judul SEO, deskripsi meta, slug), lalu jalankan Gerbang Kualitas: `{{PYTHON}} -I -X utf8 alat/cek-artikel.py "<artikel>"`. Verifikasi bahasa sudah otomatis (wordlist offline). Perbaiki hanya bagian FAIL sampai 0 FAIL. Jangan rombak keseluruhan.
6. Draft asli tidak boleh ditimpa. Ledger dan laporan ditulis ke `LAPORAN.md` folder bulan klien, bukan ke `AGENT.md`. Hash ledger disalin dari keluaran skrip, tidak dihitung manual.
7. **ZeroGPT dipindai operator (manusia)**: siapkan teks prosa siap tempel (≤15.000 karakter per bagian, pecah di batas paragraf bila perlu), serahkan ke operator berserta URL ZeroGPT, lalu minta hasil per artikel (verdict + angka AI%). Bila di atas 10% per artikel: perbaiki bagian yang ditandai, lalu minta operator memindai ulang — ulangi sampai di bawah 10% atau operator menghentikan.
8. Jangan menyatakan artikel lulus sebelum gerbang kualitas terbaru menunjukkan `0 FAIL` pada berkas terbaru, dan jangan mengarang angka ZeroGPT — catat hasil operator apa adanya.
9. Akhiri dengan laporan ringkas di chat: status setiap draft (termasuk yang dilewati), tabel artikel yang diproses, temuan yang butuh keputusan, dan status plagiarisme.
