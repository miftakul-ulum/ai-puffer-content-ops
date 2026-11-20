#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Uji otomatis kedua gerbang (cek-status.py dan cek-artikel.py).

Pakai: python3 -I -X utf8 alat/uji-tools.py
Semua skenario dibuat di folder sementara; tidak menyentuh data klien.

Author: Mas Wondho - Duta Corpora Indonesia (DCI)
Copyright (c) 2026 Duta Corpora Indonesia - All rights reserved
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = [sys.executable, "-I", "-X", "utf8"]
GAGAL_UJI = []


def jalankan(*argv):
    r = subprocess.run(PY + [str(a) for a in argv], capture_output=True, text=True, timeout=300)
    return r.returncode, (r.stdout + r.stderr)


def cek(nama, kondisi, detail=""):
    status = "OK  " if kondisi else "GAGAL"
    print("%s %s %s" % (status, nama, detail))
    if not kondisi:
        GAGAL_UJI.append(nama)


def bikin_skenario(base):
    klien = base / "Klien Uji"
    bulan = klien / "artikel" / "2026 Maret"
    bulan.mkdir(parents=True, exist_ok=True)
    (klien / "CLIENT.md").write_text(
        "# CLIENT.md\n\n"
        "| Field Placeholder | Isi |\n|---|---|\n"
        "| `{client_name}` | Klien Uji |\n"
        "| `{client_url}` | https://klienuji.example |\n"
        "| `{client_phone}` | +62 000 |\n"
        "| `{client_email}` | a@b.example |\n"
        "| `{client_wa_shortcode}` | `[wa id=\"9\"]` |\n"
        "| Istilah dipertahankan | Blitar |\n", encoding="utf8")
    return klien, bulan


def uji_status(base):
    klien, bulan = bikin_skenario(base)
    (bulan / "selesai.txt").write_text("lengkap\n[wa id=\"9\"]\n", encoding="utf8")
    (bulan / "lanjut.txt").write_text("sebagian\n[wa id=\"9\"]\n", encoding="utf8")
    (bulan / "menunggu.txt").write_text("belum selesai\n", encoding="utf8")
    # hash diambil dari output skrip supaya sama cara hitungnya
    kode, out = jalankan(ROOT / "alat" / "cek-status.py", bulan)
    cek("status: skrip jalan", kode == 0, out[:80])
    h = {nama: hh for hh, nama in re.findall(r"\t([0-9a-f]{16})\t[^\t]*\t(\S+\.txt)", out)}
    (bulan / "LAPORAN.md").write_text(
        "| Draft | Hash | Audit | Humanize | ZeroGPT |\n|---|---|---|---|---|\n"
        "| selesai.txt | %s | 2026-03-01 | 2026-03-01 | 3%% AI |\n"
        "| lanjut.txt | %s | 2026-03-01 | - | - |\n"
        % (h.get("selesai.txt", "0" * 16), h.get("lanjut.txt", "0" * 16)), encoding="utf8")
    kode, out = jalankan(ROOT / "alat" / "cek-status.py", bulan)
    cek("status: SELESAI terdeteksi", "SELESAI" in out and "selesai.txt" in out)
    cek("status: LANJUTKAN menunjukkan tahap kosong", re.search(r"LANJUTKAN\s+\S+\ttahap_kosong=humanize,zerogpt\tlanjut.txt", out) is not None)
    cek("status: MENUNGGU untuk draft tanpa shortcode", re.search(r"MENUNGGU\t\S+\ttahap_kosong=-\tmenunggu.txt", out) is not None)
    (klien / "CLIENT.md").unlink()
    kode, out = jalankan(ROOT / "alat" / "cek-status.py", bulan)
    cek("status: tanpa CLIENT.md -> gagal jelas", kode != 0 and "CLIENT.md" in out)


MINI = (
    '<p><a href="https://klienuji.example/artikel/mini"><b><i>Kata Kunci Uji</i></b></a> - Paragraf pembuka. '
    + "Kalimat isi yang cukup panjang untuk dihitung. " * 6 + '</p>\n\n'
    "<p>&nbsp;</p>\n<h2>Bagian</h2>\n"
    + ("Paragraf seragam satu. Paragraf seragam dua. Paragraf seragam tiga.\n\n" * 8)
    + "Harga mulai Rp5000 saja tanpa label.\n[wa id=\"9\"]\n"
)


def uji_artikel(base):
    _, bulan = bikin_skenario(base)
    mini = bulan / "mini.txt"
    mini.write_text(MINI, encoding="utf8")
    skrip = ROOT / "alat" / "cek-artikel.py"
    kode, out = jalankan(skrip, mini, "--kw", "Kata Kunci Uji")
    cek("artikel: gerbang menolak draft cacat (exit 1)", kode == 1)
    cek("artikel: FAIL jumlah kata", re.search(r"FAIL.*jumlah kata \d+ < 2000", out) is not None)
    cek("artikel: FAIL h2 tanpa nbsp/detail heading", "FAIL" in out)
    cek("artikel: FAIL angka tanpa label", "Rp5000" in out or "angka" in out.lower())
    kode, out = jalankan(skrip, mini, "--kw", "Kata Kunci Uji", "--draft")
    cek("artikel: mode draft exit 0", kode == 0)
    cek("artikel: mode draft mengeluarkan TEMUAN bernomor", re.search(r"TEMUAN\s+\d+:", out) is not None)
    cek("artikel: draft menandai ritme paragraf seragam", "ritme paragraf seragam" in out)

    # Regresi: 'Anda' kapital sah di awal kalimat/paragraf, salah di tengah kalimat.
    anda = bulan / "anda.txt"
    anda.write_text(MINI + "\nAnda bisa menghubungi kami. Silakan hubungi sekarang. Anda siap?\n"
                    "Jika Anda butuh bantuan, kami siap.\n", encoding="utf8")
    kode, out = jalankan(skrip, anda, "--kw", "Kata Kunci Uji", "--draft")
    # Konteks temuan bisa memuat baris baru, jadi tangkap sampai TEMUAN/INFO/garis berikutnya.
    salah = re.findall(r"'Anda' kapital di tengah kalimat: (.*?)(?=\nTEMUAN|\nINFO|\n-{10})", out, re.S)
    cek("artikel: tepat 1 'Anda' salah ditandai (dari 3 kemunculan)", len(salah) == 1, "ditandai=%d" % len(salah))
    cek("artikel: yang ditandai adalah 'Jika Anda' di tengah kalimat", len(salah) == 1 and "Jika Anda" in salah[0], str(salah))

    # Regresi: draft tanpa anchor permalink tetap exit 0 (kontrak mode audit).
    polos = bulan / "polos.txt"
    polos.write_text("Draft polos tanpa anchor permalink.\n[wa id=\"9\"]\n", encoding="utf8")
    kode, out = jalankan(skrip, polos, "--draft")
    cek("artikel: draft tanpa anchor exit 0", kode == 0, "exit=%d" % kode)
    cek("artikel: draft tanpa anchor dilaporkan sebagai temuan", "anchor permalink" in out)
    kode, out = jalankan(skrip, polos)
    cek("artikel: gerbang final tanpa keyword tetap gagal (exit 2)", kode == 2, "exit=%d" % kode)


KW = "Kata Kunci Uji"
KALIMAT = [
    "Kegiatan rapat berjalan lancar dan para peserta menikmati hidangan yang tersaji dengan rapi.",
    "Panitia menyiapkan jadwal sejak pagi supaya setiap tamu mendapat giliran yang adil.",
    "Pengantaran dilakukan tepat waktu sehingga acara tidak tertunda oleh urusan konsumsi.",
    "Setiap menu dipilih dengan melihat selera peserta dan kebiasaan makan di daerah setempat.",
    "Pertanyaan yang paling sering muncul adalah soal jumlah porsi dan waktu pemesanan.",
    "Tim dapur memeriksa bahan sebelum dimasak agar rasa tetap terjaga sampai ke meja.",
    "Kemasan dibuat rapat sehingga makanan tetap hangat selama perjalanan menuju lokasi.",
    "Pemesan biasanya menghubungi kami beberapa hari sebelum kegiatan dimulai.",
]


def kalimat(n, mulai=0):
    return " ".join(KALIMAT[(mulai + i) % len(KALIMAT)] for i in range(n))


def artikel_lulus():
    """Artikel sintetis yang harus lolos gerbang final dengan 0 FAIL."""
    p1 = ('<p><a href="https://klienuji.example/artikel/kata-kunci-uji"><b><i>%s</i></b></a> - %s '
          '<a href="https://klienuji.example" target="_blank" rel="noopener"><b>Klien Uji</b></a> '
          'melayani wilayah <a href="https://id.wikipedia.org/wiki/Blitar" target="_blank" '
          'rel="noopener noreferrer">Blitar</a>.</p>' % (KW, kalimat(17)))
    gambar = ('<div style="border: 2px dashed #ff6600;">\n<strong>GAMBAR DISINI</strong><br> '
              '<em>Saran: foto hidangan tersaji di meja rapat\n</em><br> '
              '<small>Alt text: "%s - hidangan tersaji di meja rapat"</small>\n</div>' % KW)
    bagian = [p1, "<!--more-->", gambar]
    n_bold = 0
    for i in range(1, 8):
        judul = "Panduan %s Bagian %d" % (KW, i) if i <= 3 else "Catatan Pemesanan Bagian %d" % i
        bagian += ["<p>&nbsp;</p>", "<h2>%s</h2>" % judul]
        for j in range(4):
            if n_bold < 28:
                bagian.append("<p>%s <b>%s</b> %s</p>" % (kalimat(3, i + j), KW, kalimat(4, i + j + 3)))
                n_bold += 1
            else:
                bagian.append("<p>%s</p>" % kalimat(7, i + j))
        if i == 2:
            bagian.append("<ul>\n<li>Jadwal pengantaran</li>\n<li>Jumlah porsi</li>\n</ul>")
    bagian += ["<p>&nbsp;</p>", "<h2>Hubungi Kami Dari Kontak Resmi Klien Uji</h2>",
               "<b>WA:</b> +62 000\n<b>Telepon:</b> +62 000\n<b>Email:</b> a@b.example",
               "<p>Terima kasih sudah membaca sampai selesai.</p>", '[wa id="9"]']
    return "\n\n".join(bagian) + "\n"


def uji_artikel_lulus(base):
    _, bulan = bikin_skenario(base)
    skrip = ROOT / "alat" / "cek-artikel.py"
    lulus = bulan / "lulus.txt"
    lulus.write_text(artikel_lulus(), encoding="utf8")
    kode, out = jalankan(skrip, lulus)
    cek("lulus: artikel sehat 0 FAIL (exit 0)", kode == 0 and "0 FAIL" in out, out[-160:].replace("\n", " | "))

    # Mutasi: tiap perubahan kecil harus membuat gerbang menolak.
    isi = artikel_lulus()
    # (teks mutasi, potongan pesan FAIL yang wajib muncul)
    mutasi = {
        "ejaan tidak baku di awal kalimat": (isi.replace("<p>Terima kasih", "<p>Silahkan hubungi kami. Terima kasih"), "ejaan tidak baku: 'silahkan'"),
        "kata asing di awal kalimat": (isi.replace("<p>Terima kasih", "<p>Snack Box tersedia. Terima kasih"), "kata asing: 'snack'"),
        "more-tag hilang": (isi.replace("<!--more-->", ""), "<!--more--> ada 0"),
        "shortcode WA hilang": (isi.replace('\n\n[wa id="9"]', ""), "baris terakhir bukan shortcode"),
        "keyword body tidak dibold": (isi.replace("<b>%s</b>" % KW, KW, 1), "hanya"),
    }
    for nama, (teks, pesan) in mutasi.items():
        f = bulan / "mutasi.txt"
        f.write_text(teks, encoding="utf8")
        kode, out = jalankan(skrip, f)
        cek("lulus: mutasi '%s' ditolak" % nama, kode == 1 and pesan in out, "exit=%d" % kode)


META_BAIK = ("Judul SEO: Kata Kunci Uji | Klien Uji\n"
             "Deskripsi meta: Kata Kunci Uji untuk kebutuhan rapat dan acara kantor di Blitar.\n"
             "Slug: kata-kunci-uji\n")


def uji_meta(base):
    _, bulan = bikin_skenario(base)
    skrip = ROOT / "alat" / "cek-artikel.py"
    art = bulan / "lulus - Humanized.txt"
    art.write_text(artikel_lulus(), encoding="utf8")
    meta = bulan / "lulus - Meta.txt"                       # nama dasar = nama artikel tanpa " - Humanized"

    kode, out = jalankan(skrip, art)
    cek("meta: tanpa berkas meta hanya WARN, bukan FAIL", kode == 0 and "berkas meta" in out, "exit=%d" % kode)

    meta.write_text(META_BAIK, encoding="utf8")
    kode, out = jalankan(skrip, art)
    cek("meta: berkas meta benar lolos 0 FAIL", kode == 0 and "0 FAIL" in out, out[-120:].replace("\n", " | "))

    kasus = {
        "judul SEO tanpa keyword": (META_BAIK.replace("Judul SEO: Kata Kunci Uji", "Judul SEO: Judul Lain"), "judul SEO tidak memuat keyword"),
        "deskripsi tanpa keyword": (META_BAIK.replace("Deskripsi meta: Kata Kunci Uji untuk", "Deskripsi meta: Layanan untuk"), "deskripsi meta tidak memuat keyword"),
        "slug tanpa keyword": (META_BAIK.replace("Slug: kata-kunci-uji", "Slug: nama-lain"), "tidak memuat keyword"),
        "slug berbeda dari anchor": (META_BAIK.replace("Slug: kata-kunci-uji", "Slug: kata-kunci-uji-lengkap"), "berbeda dari slug di anchor"),
        "slug berhuruf besar": (META_BAIK.replace("Slug: kata-kunci-uji", "Slug: Kata-Kunci-Uji"), "bukan huruf kecil"),
        "field kosong": (META_BAIK.replace("Slug: kata-kunci-uji", "Slug:"), "field 'slug' kosong"),
    }
    for nama, (teks, pesan) in kasus.items():
        meta.write_text(teks, encoding="utf8")
        kode, out = jalankan(skrip, art)
        cek("meta: %s ditolak" % nama, kode == 1 and pesan in out, "exit=%d" % kode)

    meta.write_text(META_BAIK.replace("Kata Kunci Uji | Klien Uji", "Kata Kunci Uji | Termurah"), encoding="utf8")
    kode, out = jalankan(skrip, art)
    cek("meta: klaim 'termurah' hanya WARN", kode == 0 and "superlatif 'termurah'" in out, "exit=%d" % kode)


def uji_lintas(base):
    skrip = ROOT / "alat" / "cek-artikel.py"
    awal = artikel_lulus()
    # klien A: dua artikel; klien B: satu artikel. CLIENT.md hanya perlu ada untuk klien A.
    klien_a, bulan_a = bikin_skenario(base)
    (bulan_a / "satu - Humanized.txt").write_text(awal, encoding="utf8")
    kode, out = jalankan(skrip, bulan_a / "satu - Humanized.txt")
    cek("lintas: artikel tunggal tidak bentrok dengan dirinya", kode == 0 and "kanibalisasi" not in out and "disalin" not in out, "exit=%d" % kode)

    # keyword sama di klien yang sama -> FAIL kanibalisasi
    kedua = awal.replace("kata-kunci-uji", "kata-kunci-uji-dua")
    (bulan_a / "dua - Humanized.txt").write_text(kedua, encoding="utf8")
    kode, out = jalankan(skrip, bulan_a / "dua - Humanized.txt")
    cek("lintas: keyword sama di klien sama ditolak (kanibalisasi)", kode == 1 and "kanibalisasi" in out, "exit=%d" % kode)

    # kalimat identik di klien lain -> FAIL kalimat disalin, tetapi BUKAN kanibalisasi (beda situs)
    klien_b = base / "Klien Lain"
    bulan_b = klien_b / "artikel" / "2026 April"
    bulan_b.mkdir(parents=True)
    (klien_b / "CLIENT.md").write_text(
        "| `{client_name}` | Klien Lain |\n| `{client_url}` | https://lain.example |\n"
        "| `{client_wa_shortcode}` | `[wa id=\"9\"]` |\n| `{client_phone}` | +62 000 |\n"
        "| `{client_email}` | a@b.example |\n", encoding="utf8")
    salinan = awal.replace("klienuji.example", "lain.example").replace("Klien Uji", "Klien Lain")
    (bulan_b / "tiga - Humanized.txt").write_text(salinan, encoding="utf8")
    kode, out = jalankan(skrip, bulan_b / "tiga - Humanized.txt")
    cek("lintas: kalimat disalin dari klien lain ditolak", kode == 1 and "kalimat disalin" in out, "exit=%d" % kode)
    cek("lintas: keyword sama beda klien BUKAN kanibalisasi", "kanibalisasi" not in out)

    # artikel yang benar-benar berbeda lolos
    beda = awal
    for i, k in enumerate(KALIMAT):
        beda = beda.replace(k, "Kalimat pengganti nomor %d dengan susunan lain sama sekali agar tidak identik." % i)
    beda = beda.replace("Kata Kunci Uji", "Topik Berbeda Sekali").replace("kata-kunci-uji", "topik-berbeda-sekali")
    (bulan_b / "empat - Humanized.txt").write_text(beda, encoding="utf8")
    (bulan_b / "tiga - Humanized.txt").unlink()
    kode, out = jalankan(skrip, bulan_b / "empat - Humanized.txt", "--kw", "Topik Berbeda Sekali")
    cek("lintas: artikel berbeda tidak ditandai salin/kanibalisasi", "disalin" not in out and "kanibalisasi" not in out, "exit=%d" % kode)

    # folder berawalan _ (cetakan) diabaikan
    tmpl = base / "_TEMPLATE" / "artikel" / "YYYY Bulan"
    tmpl.mkdir(parents=True)
    (tmpl / "cetakan - Humanized.txt").write_text(awal, encoding="utf8")
    (bulan_a / "dua - Humanized.txt").unlink()
    kode, out = jalankan(skrip, bulan_a / "satu - Humanized.txt")
    cek("lintas: folder _TEMPLATE diabaikan", "_TEMPLATE" not in out, "exit=%d" % kode)


def uji_template_belum_diisi(base):
    """Klien baru yang menyalin _TEMPLATE tapi belum mengisi CLIENT.md harus dapat pesan jelas."""
    templat = ROOT / "klien" / "_TEMPLATE"
    klien = base / "klien" / "Klien Baru"
    shutil.copytree(templat, klien)
    bulan = klien / "artikel" / "YYYY Bulan"
    (bulan / "draft.txt").write_text("isi\n[whatsapp_button id=\"1\"]\n", encoding="utf8")
    kode, out = jalankan(ROOT / "alat" / "cek-status.py", bulan)
    cek("template: cek-status menolak CLIENT.md bawaan dengan pesan jelas", kode != 0 and "isian bawaan template" in out and "Traceback" not in out, "exit=%d" % kode)
    art = bulan / "a - Humanized.txt"
    art.write_text('<p><a href="https://x.example/artikel/k"><b><i>Kata</i></b></a> - isi.</p>\n', encoding="utf8")
    kode, out = jalankan(ROOT / "alat" / "cek-artikel.py", art, "--kw", "Kata")
    cek("template: cek-artikel menolak CLIENT.md bawaan (exit 2), bukan FAIL menyesatkan", kode == 2 and "isian bawaan template" in out and "tidak muncul di artikel" not in out, "exit=%d" % kode)


def uji_pasang_perintah(base):
    """Pemasang perintah: format per agent benar, placeholder terganti, tidak menyentuh berkas lain."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("pasang_uji", ROOT / "alat" / "pasang-perintah.py")
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)

    sumber = (ROOT / "perintah" / "artikel.md").read_text(encoding="utf8")
    cek("perintah: sumber netral tidak memuat kepala (---) khusus agent", not sumber.lstrip().startswith("---"))
    cek("perintah: sumber memuat penanda yang akan diganti", "{{ARGUMEN}}" in sumber and "{{PYTHON}}" in sumber)
    cek("perintah: sumber tidak merujuk folder agent (.trae/.zcode/.claude)", not re.search(r"\.(trae|zcode|claude)/", sumber))
    cek("perintah: sumber merujuk alat/ yang ada", "alat/cek-artikel.py" in sumber and (ROOT / "alat" / "cek-artikel.py").is_file())

    for nama, info in modul.AGEN.items():
        isi = modul.bangun(info)
        cek("perintah[%s]: tidak ada penanda tersisa" % nama, "{{" not in isi)
        kepala = isi.split("---")[1]
        if info["kepala"] == "trae":
            cek("perintah[trae]: kepala memakai Name dan Description", "Name: artikel" in kepala and "Description:" in kepala)
        else:
            cek("perintah[%s]: kepala memakai description dan argument-hint" % nama,
                "description:" in kepala and "argument-hint:" in kepala)
        cek("perintah[%s]: argumen disisipkan sesuai agent" % nama, info["argumen"] in isi)

    # Pasang ke folder sementara: salinan root palsu supaya repo asli tidak disentuh.
    akar = base / "root"
    (akar / "perintah").mkdir(parents=True)
    (akar / "alat").mkdir()
    shutil.copy(ROOT / "perintah" / "artikel.md", akar / "perintah" / "artikel.md")
    shutil.copy(ROOT / "alat" / "pasang-perintah.py", akar / "alat" / "pasang-perintah.py")
    asing = akar / ".claude" / "commands" / "milik-orang.md"
    asing.parent.mkdir(parents=True)
    asing.write_text("jangan disentuh", encoding="utf8")
    skrip = akar / "alat" / "pasang-perintah.py"
    kode, out = jalankan(skrip, "semua")
    cek("pasang: semua agent terpasang (exit 0)", kode == 0 and out.count("terpasang:") == 3, "exit=%d" % kode)
    cek("pasang: file perintah ada di tiap folder agent",
        all((akar / d / "commands" / "artikel.md").is_file() for d in (".trae", ".zcode", ".claude")))
    cek("pasang: command milik orang lain tidak disentuh", asing.read_text(encoding="utf8") == "jangan disentuh")
    cek("pasang: akhir baris LF", b"\r" not in (akar / ".trae" / "commands" / "artikel.md").read_bytes())
    kode, out = jalankan(skrip, "semua", "--cek")
    cek("pasang: --cek melaporkan sudah terbaru", kode == 0 and out.count("sudah terpasang dan terbaru") == 3, out[:100].replace("\n", " | "))
    (akar / ".zcode" / "commands" / "artikel.md").write_text("usang", encoding="utf8")
    kode, out = jalankan(skrip, "zcode", "--cek")
    cek("pasang: --cek mendeteksi salinan usang tanpa menulis", "berbeda" in out and (akar / ".zcode" / "commands" / "artikel.md").read_text(encoding="utf8") == "usang")
    kode, out = jalankan(skrip, "gemini")
    cek("pasang: agent tidak dikenal ditolak (exit 2)", kode == 2 and "tidak dikenal" in out, "exit=%d" % kode)
    kode, out = jalankan(skrip)
    cek("pasang: tanpa argumen menampilkan daftar (exit 2)", kode == 2 and "Agent yang didukung" in out, "exit=%d" % kode)
    (akar / "perintah" / "artikel.md").unlink()
    kode, out = jalankan(skrip, "trae")
    cek("pasang: sumber hilang -> pesan jelas (exit 2)", kode == 2 and "tidak ada" in out and "Traceback" not in out, "exit=%d" % kode)


def uji_masukan_buruk(base):
    """Masukan yang salah harus menghasilkan pesan manusiawi dengan kode 2, bukan traceback."""
    _, bulan = bikin_skenario(base)
    skrip = ROOT / "alat" / "cek-artikel.py"
    kode, out = jalankan(skrip, bulan / "tidak-ada.txt")
    cek("masukan: berkas tidak ada -> pesan jelas, exit 2", kode == 2 and "tidak ada" in out and "Traceback" not in out, "exit=%d" % kode)
    rusak = bulan / "latin1.txt"
    rusak.write_bytes(b"<p>\xe9\xe8</p>")
    kode, out = jalankan(skrip, rusak, "--kw", "x")
    cek("masukan: bukan UTF-8 -> pesan jelas, exit 2", kode == 2 and "UTF-8" in out and "Traceback" not in out, "exit=%d" % kode)
    kosong = bulan / "kosong.txt"
    kosong.write_text("", encoding="utf8")
    kode, out = jalankan(skrip, kosong, "--draft")
    cek("masukan: draft kosong tetap exit 0 (audit bukan penghalang)", kode == 0 and "Traceback" not in out, "exit=%d" % kode)
    kode, out = jalankan(ROOT / "alat" / "cek-status.py", bulan)
    cek("masukan: cek-status tidak crash, draft kosong = MENUNGGU", kode == 0 and "MENUNGGU" in out and "Traceback" not in out, "exit=%d" % kode)
    cek("masukan: cek-status melaporkan berkas bukan UTF-8 sebagai RUSAK, draft lain tetap terbaca",
        re.search(r"RUSAK\t-\ttahap_kosong=-\tlatin1\.txt", out) is not None and "kosong.txt" in out, out[:120].replace("\n", " | "))


class HalamanPalsu:
    def __init__(self, html_teks):
        self.html_teks = html_teks

    def read(self):
        return self.html_teks.encode("utf8")


def uji_kbbi():
    """kbbi_cek diuji dengan halaman palsu (tanpa jaringan)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("cek_artikel_uji", ROOT / "alat" / "cek-artikel.py")
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    asli = modul.ureq.urlopen
    kasus = {
        "halaman kuota harian -> KUOTA (bukan dibaca sebagai kata)":
            ("<h2>Pencarian Anda telah mencapai batas maksimum dalam sehari</h2>", "KUOTA"),
        "entri tidak ditemukan -> TIDAK_ADA": ("<p>Entri tidak ditemukan</p>", "TIDAK_ADA"),
        "entri sah -> OK": ("<h2>kata</h2>", "OK"),
        "halaman tanpa h2 -> ERROR": ("<p>kosong</p>", "ERROR"),
    }
    try:
        for nama, (halaman, harap) in kasus.items():
            modul.ureq.urlopen = lambda *a, _h=halaman, **k: HalamanPalsu(_h)
            status, _ = modul.kbbi_cek("kata")
            cek("kbbi: " + nama, status == harap, "status=%s" % status)
    finally:
        modul.ureq.urlopen = asli


def main():
    with tempfile.TemporaryDirectory(prefix="uji-dci-seo-") as d:
        base = Path(d)
        uji_status(base)
        uji_artikel(base)
        uji_artikel_lulus(base)
    with tempfile.TemporaryDirectory(prefix="uji-dci-pasang-") as d:
        uji_pasang_perintah(Path(d))
    with tempfile.TemporaryDirectory(prefix="uji-dci-templat-") as d:
        uji_template_belum_diisi(Path(d))
    with tempfile.TemporaryDirectory(prefix="uji-dci-masukan-") as d:
        uji_masukan_buruk(Path(d))
    with tempfile.TemporaryDirectory(prefix="uji-dci-meta-") as d:
        uji_meta(Path(d))
    with tempfile.TemporaryDirectory(prefix="uji-dci-lintas-") as d:
        uji_lintas(Path(d))
    uji_kbbi()
    print("-" * 60)
    if GAGAL_UJI:
        print("UJI GAGAL: %s" % ", ".join(GAGAL_UJI))
        sys.exit(1)
    print("Semua uji lulus.")


main()
