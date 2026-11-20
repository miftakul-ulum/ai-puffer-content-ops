#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DCI SEO Auditor - gerbang kualitas artikel: Rank Math + format WordPress + Anti-Typo Gate.

Pakai (dari ROOT project):
  python3 -I -X utf8 alat/cek-artikel.py "klien/<Klien>/artikel/<YYYY Bulan>/<Slug> - Humanized.txt"
  Opsi:
    --kw "Fokus Keyword"   batalin deteksi otomatis (default: anchor permalink pertama)

Verifikasi bahasa berjalan OFFLINE: kamus approved (kamus-kata.txt) + wordlist KBBI
(kamus-kbbi-offline.txt, 112.651 kata). Tidak ada panggilan jaringan di skrip ini.
Kata yang tidak ditemukan di keduanya dilaporkan sebagai REVIEW untuk tinjauan manual.

Author: Mas Wondho - Duta Corpora Indonesia (DCI)
Copyright (c) 2026 Duta Corpora Indonesia - All rights reserved
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KAMUS = ROOT / "alat" / "kamus-kata.txt"
WORDLIST = ROOT / "alat" / "kamus-kbbi-offline.txt"
VOID = {"br", "img", "hr", "meta", "link", "input", "source"}
RE_KATA = re.compile(r"[a-zà-ÿ]+(?:-[a-zà-ÿ]+)*")

# Ejaan tidak baku (semua sudah dicek KBBI; entri KBBI mengarah ke bentuk baku)
NON_BAKU = {
    "silahkan": "silakan", "resiko": "risiko", "merubah": "mengubah",
    "aktifitas": "aktivitas", "analisa": "analisis", "apotik": "apotek",
    "nafas": "napas", "ijin": "izin", "kwalitas": "kualitas",
    "mengkonsumsi": "mengonsumsi", "mempengaruhi": "memengaruhi",
    "capcay": "capcai", "nasehat": "nasihat", "praktek": "praktik",
    "propinsi": "provinsi", "jaman": "zaman", "sambel": "sambal",
}
# Kata asing umum yang memang tidak ada di KBBI (contoh terverifikasi 2026-11-20)
KATA_ASING = {"snack", "box", "coffee", "break", "dessert", "price", "cheap",
              "booking", "package", "service", "quality", "best", "order"}
KLICHE = ["di era modern ini", "dalam dunia yang semakin berkembang",
          "tidak dapat dipungkiri", "perlu diketahui bahwa", "sangat penting untuk",
          "merupakan salah satu", "berbagai macam", "memainkan peran penting"]
ANCHOR_DATAR = ["klik di sini", "baca selengkapnya", "halaman ini", "di sini"]
MARKER_PERCAKAPAN = ["nah,", "jujur saja", "sebenarnya,", "kalau menurut pengalaman",
                     "percaya atau tidak", "coba bayangkan", "mungkin anda bertanya-tanya",
                     "anda pasti pernah"]


def baca_kamus():
    if not KAMUS.exists():
        return set()
    return {b.strip().lower() for b in KAMUS.read_text(encoding="utf8").splitlines()
            if b.strip() and not b.startswith("#")}


def baca_wordlist():
    """Wordlist KBBI offline (112.651 kata). Tidak ada berkas = set kosong (semua jadi REVIEW)."""
    if not WORDLIST.exists():
        return set()
    return {b.strip().lower() for b in WORDLIST.read_text(encoding="utf8", errors="replace").splitlines()
            if b.strip() and not b.startswith("#")}


def dasar_kandidat(kata):
    """Kandidat bentuk dasar: lepas akhiran lalu awalan umum (reguler, tanpa morfologi penuh)."""
    kandidat = {kata}
    for suf in ("nya", "kan", "an", "i", "lah", "kah", "pun"):
        if kata.endswith(suf) and len(kata) > len(suf) + 3:
            kandidat.add(kata[:-len(suf)])
    for tanpa_suf in list(kandidat):
        for pre in ("meng", "meny", "men", "mem", "me", "peng", "peny", "pen", "pem",
                    "pe", "ber", "be", "di", "ter", "ke", "se"):
            if tanpa_suf.startswith(pre) and len(tanpa_suf) > len(pre) + 2:
                dasar = tanpa_suf[len(pre):]
                kandidat.add(dasar)
                if pre in ("meny", "peny"):
                    kandidat.add("s" + dasar)
                if pre in ("peng", "pem"):
                    kandidat.add("p" + dasar)
    return kandidat


def baca_client(folder_bulan):
    client = folder_bulan.parent.parent / "CLIENT.md"
    data = {}
    if client.exists():
        t = client.read_text(encoding="utf8")
        pasangan = {
            "client_name": "nama", "client_url": "url", "client_phone": "telepon",
            "client_email": "email", "client_wa_shortcode": "shortcode",
            "Istilah dipertahankan": "istilah",
        }
        for kunci, alias in pasangan.items():
            m = re.search(r"\|\s*`?\{?" + re.escape(kunci) + r"\}?`?\s*\|\s*([^|]+)\|", t)
            if m:
                data[alias] = m.group(1).strip().strip("`")
    return data


def teks_tampak(raw):
    t = re.sub(r"<img[^>]*>", " ", raw)                      # alt tidak dihitung Rank Math
    t = re.sub(r"<div.*?</div>", " ", t, flags=re.S)          # blok GAMBAR DISINI (editor saja)
    t = re.sub(r"<[^>]+>", " ", t).replace("&nbsp;", " ")
    t = re.sub(r"https?://\S+", " ", t)
    t = "\n".join(b for b in t.split("\n") if "whatsapp_button" not in b)
    t = re.sub(r"\s+([,.!?;:])", r"\1", t)                    # spasi sebelum tanda baca = artefak strip tag
    return re.sub(r"[ \t]+", " ", t)


def tag_seimbang(raw):
    masalah, tumpuk = [], []
    for m in re.finditer(r"<(/?)([a-zA-Z0-9]+)[^>]*?(/?)>", raw):
        tutup, nama, sendiri = m.group(1), m.group(2).lower(), m.group(3)
        if nama in VOID or sendiri:
            continue
        if tutup:
            if not tumpuk or tumpuk[-1] != nama:
                masalah.append("</%s> tanpa pasangan di posisi %d" % (nama, m.start()))
            else:
                tumpuk.pop()
        else:
            tumpuk.append(nama)
    for sisa in tumpuk:
        masalah.append("<%s> tidak pernah ditutup" % sisa)
    return masalah


def cek_bahasa(teks, izin):
    gagal, peringatan, unik = [], [], sorted({w.lower() for w in RE_KATA.findall(teks.lower())})
    sah = kamus | wordlist
    for kata in unik:
        if kata in izin:
            continue
        bagian = kata.split("-")
        terverifikasi = kata in sah or all(b in sah for b in bagian)
        if not terverifikasi:
            # Normalisasi imbuhan: kata berimbuhan reguler dicocokkan ke bentuk dasarnya.
            if not any(k in sah for k in dasar_kandidat(kata)):
                peringatan.append(kata)
    # Tanpa peka kapital: kata di awal kalimat ("Silahkan ...") tetap tertangkap.
    # Kata dari "Istilah dipertahankan"/nama klien/fokus keyword (izin) dikecualikan.
    for kata, baku in sorted(NON_BAKU.items()):
        if kata not in izin and re.search(r"\b" + kata + r"\b", teks, re.I):
            gagal.append("ejaan tidak baku: '%s' -> '%s'" % (kata, baku))
    for kata in sorted(KATA_ASING):
        if kata not in izin and re.search(r"\b" + kata + r"\b", teks, re.I):
            gagal.append("kata asing: '%s' (ganti padanan Indonesia baku)" % kata)
    for frasa in KLICHE:
        if frasa in teks.lower():
            gagal.append("kliche terlarang: '%s'" % frasa)
    for m in re.finditer(r"[—–]", teks):
        gagal.append("em/en dash di posisi %d" % m.start())
    for m in re.finditer(r"[“”‘’]", teks):
        gagal.append("tanda kutip miring di posisi %d" % m.start())
    for m in re.finditer(r"\bAnda\b", teks):
        sebelum = teks[:m.start()]
        isi = sebelum.rstrip()
        jeda = sebelum[len(isi):]
        if not isi or "\n" in jeda or isi[-1] in ".!?":
            continue                                      # awal kalimat/paragraf: kapital sah
        gagal.append("'Anda' kapital di tengah kalimat: ...%s" % teks[max(0, m.start() - 25):m.start() + 8])
    for m in re.finditer(r"\b([a-zà-ÿ]{3,}) \1\b", teks):
        gagal.append("kata kembar: '%s %s'" % (m.group(1), m.group(1)))
    for m in re.finditer(r" [,.!?;:]", teks):
        peringatan.append("spasi sebelum tanda baca: ...%s" % teks[max(0, m.start() - 20):m.start() + 6])
    for m in re.finditer(r"\b(klik di sini|baca selengkapnya|halaman ini|di sini)\b", teks):
        peringatan.append("anchor datar: '%s'" % m.group(1))
    return gagal, peringatan, unik


def analisis_ritme(raw):
    """Analisis pola khas tulisan AI pada draft mentah (bahan Tahap 3 humanize)."""
    temuan = []
    baris = [l for l in raw.split("\n")
             if l.strip() and not l.strip().startswith(("<", "&nbsp;", "[", "<!--"))]
    kalimat_per_para = []
    for l in baris:
        teks = re.sub(r"<[^>]+>", " ", l)
        n = len([s for s in re.split(r"(?<=[.!?])\s+", teks) if s.strip()])
        kalimat_per_para.append(n)
    if len(kalimat_per_para) >= 6:
        sama = sum(1 for i in range(1, len(kalimat_per_para))
                   if kalimat_per_para[i] == kalimat_per_para[i - 1])
        if sama >= len(kalimat_per_para) * 0.4:
            temuan.append("ritme paragraf seragam: %d dari %d paragraf berurutan punya jumlah kalimat sama (variasikan 1-7 kalimat)" % (sama, len(kalimat_per_para)))
    semua_kalimat = []
    for l in baris:
        teks = re.sub(r"<[^>]+>", " ", l)
        semua_kalimat += [s for s in re.split(r"(?<=[.!?])\s+", teks) if s.strip()]
    if semua_kalimat:
        lens = [len(s.split()) for s in semua_kalimat]
        pendek = sum(1 for n in lens if n <= 8)
        panjang = sum(1 for n in lens if n >= 20)
        if pendek * 100.0 / len(lens) < 10:
            temuan.append("variasi kalimat kurang: hanya %d%% kalimat pendek (<=8 kata) dari %d kalimat" % (pendek * 100 // len(lens), len(lens)))
        if panjang * 100.0 / len(lens) < 5:
            temuan.append("hampir tidak ada kalimat panjang (>=20 kata): %d%% saja" % (panjang * 100 // len(lens)))
    kata_pertama = [re.sub(r"<[^>]+>", " ", l).strip().split()[0].lower() for l in baris
                    if re.sub(r"<[^>]+>", " ", l).strip()]
    for i in range(1, len(kata_pertama)):
        if kata_pertama[i] == kata_pertama[i - 1]:
            temuan.append("dua paragraf berurutan berawalan kata sama: '%s'" % kata_pertama[i])
    rendah = raw.lower()
    for m in MARKER_PERCAKAPAN:
        n = rendah.count(m)
        if n > 2:
            temuan.append("marker percakapan '%s' muncul %dx (maksimal 2)" % (m, n))
    gab = len(re.findall(r"\b[\w-]+(?: [\w-]+)?, [\w-]+(?: [\w-]+)?, (?:dan|serta|atau) [\w-]+", re.sub(r"<[^>]+>", " ", raw)))
    if gab > 10:
        temuan.append("pola 'A, B, dan C' muncul %dx (rule-of-three paksa)" % gab)
    return temuan


def cek_angka(raw):
    """Klaim angka (rupiah/persen) wajib berlabel kisaran/tergantung/perkiraan."""
    temuan = []
    for m in re.finditer(r"[^.]{0,60}\b(?:rp\.?\s?\d|\d+\s?%)[^.]{0,60}", raw, re.I):
        frasa = m.group(0)
        if not re.search(r"kisaran|tergantung|perkiraan|patokan|±", frasa, re.I):
            temuan.append("angka tanpa label kisaran/tergantung: ...%s..." % frasa.strip()[:70])
            break
    return temuan


KLAIM_SUPERLATIF = ["termurah", "terbaik", "terlengkap", "nomor 1", "no. 1", "nomor satu", "paling murah"]


def slug_dari(teks):
    return re.sub(r"[^a-z0-9]+", "-", teks.lower()).strip("-")


def cek_meta(p, raw, kw):
    """Periksa berkas pendamping '<nama> - Meta.txt' (judul SEO, deskripsi meta, slug).

    Aturan Rank Math di AGENT.md mewajibkan keyword di judul SEO, deskripsi meta, dan slug,
    tetapi ketiganya tidak ada di badan artikel. Format berkas (satu field per baris):
      Judul SEO: ...
      Deskripsi meta: ...
      Slug: ...
    """
    gagal, peringatan, info = [], [], []
    dasar = p.stem[:-len(" - Humanized")] if p.stem.endswith(" - Humanized") else p.stem
    f = p.parent / (dasar + " - Meta.txt")
    if not f.exists():
        peringatan.append("berkas meta '%s' tidak ada: keyword di judul SEO, deskripsi meta, dan slug "
                          "belum bisa diverifikasi" % f.name)
        return gagal, peringatan, info
    isi = f.read_text(encoding="utf8").replace("\r", "")
    medan = {}
    for m in re.finditer(r"^\s*(judul seo|deskripsi meta|slug)\s*:\s*(.*?)\s*$", isi, re.I | re.M):
        medan[m.group(1).lower()] = m.group(2)
    for nama in ("judul seo", "deskripsi meta", "slug"):
        if not medan.get(nama):
            gagal.append("berkas meta: field '%s' kosong atau tidak ada" % nama)
    judul, desk, slug = (medan.get(k, "") for k in ("judul seo", "deskripsi meta", "slug"))
    k = kw.lower()
    if judul and k not in judul.lower():
        gagal.append("judul SEO tidak memuat keyword '%s'" % kw)
    if judul and len(judul) > 60:
        peringatan.append("judul SEO %d karakter, di atas ±60 yang tampil di desktop (Rank Math)" % len(judul))
    if desk and k not in desk.lower():
        gagal.append("deskripsi meta tidak memuat keyword '%s'" % kw)
    elif desk and desk.lower().find(k) + len(k) > 160:
        peringatan.append("keyword di deskripsi meta berada setelah karakter ke-160 (Rank Math minta di 120-160 awal)")
    if desk and len(desk) > 160:
        info.append("deskripsi meta %d karakter: Google memotong sesuai lebar perangkat, bukan batas tetap" % len(desk))
    for teks_meta, nama in ((judul, "judul SEO"), (desk, "deskripsi meta")):
        for klaim in KLAIM_SUPERLATIF:
            if klaim in teks_meta.lower():
                peringatan.append("%s memuat klaim superlatif '%s': pastikan terbukti, atau ganti" % (nama, klaim))
    if slug:
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
            gagal.append("slug '%s' bukan huruf kecil/angka dengan tanda hubung" % slug)
        if slug_dari(kw) not in slug:
            gagal.append("slug '%s' tidak memuat keyword (%s)" % (slug, slug_dari(kw)))
        m = re.search(r'<a href="[^"]*?/([^"/]+)/?"><b><i>', raw)
        if m and m.group(1) != slug:
            gagal.append("slug meta '%s' berbeda dari slug di anchor permalink '%s'" % (slug, m.group(1)))
    return gagal, peringatan, info


RE_ANCHOR_KW = re.compile(r'<a href="[^"]*"><b><i>([^<]+)</i></b></a>')


def kata_isi(raw):
    """Kata prosa untuk perbandingan antar artikel (tanpa blok kontak boilerplate)."""
    t = teks_tampak(raw)
    t = "\n".join(b for b in t.split("\n")
                  if not re.search(r"Hubungi Kami Dari Kontak Resmi|^\s*(WA|Telepon|Email)\s*:", b))
    return re.findall(r"[a-zà-ÿ0-9]+", t.lower())


def rangkaian(kata, n=8):
    return {" ".join(kata[i:i + n]) for i in range(len(kata) - n + 1)}


def cek_lintas(p, raw, kw):
    """Bandingkan dengan artikel final lain di klien/: kanibalisasi keyword dan kalimat yang disalin.

    Kanibalisasi hanya dihitung dalam satu klien (satu situs). Kalimat yang disalin dihitung
    di semua klien: FAKTA-SEO.md poin 5 melarang menyalin kalimat antar artikel.
    """
    gagal, peringatan = [], []
    diri = p.resolve()
    folder_klien = diri.parent.parent.parent
    akar = folder_klien.parent
    punyaku = rangkaian(kata_isi(raw))
    token_kw = set(kw.lower().split())
    for f in sorted(akar.glob("*/artikel/*/* - Humanized.txt")):
        f = f.resolve()
        klien = f.parent.parent.parent
        if f == diri or klien.name.startswith("_"):
            continue
        r2 = f.read_text(encoding="utf8").replace("\r", "")
        label = "%s / %s" % (klien.name, f.stem)
        m = RE_ANCHOR_KW.search(r2)
        kw2 = m.group(1).strip() if m else ""
        if klien == folder_klien and kw2:
            if kw2.lower() == kw.lower():
                gagal.append("kanibalisasi: keyword '%s' sama dengan artikel lain di klien yang sama (%s)" % (kw, label))
            else:
                t2 = set(kw2.lower().split())
                if token_kw and t2 and len(token_kw & t2) * 1.0 / len(token_kw | t2) >= 0.6:
                    peringatan.append("keyword mirip dengan '%s' (%s): pastikan maksud pencariannya berbeda" % (kw2, label))
        bersama = len(punyaku & rangkaian(kata_isi(r2)))
        if bersama >= 3:
            gagal.append("kalimat disalin: %d rangkaian 8 kata sama dengan %s" % (bersama, label))
    return gagal, peringatan


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("artikel")
    ap.add_argument("--kw", default=None)
    ap.add_argument("--draft", action="store_true",
                    help="mode audit draft mentah: keluarkan temuan sebagai bahan humanize (exit selalu 0)")
    a = ap.parse_args()
    global kamus, wordlist
    kamus = baca_kamus()
    wordlist = baca_wordlist()
    if not wordlist:
        print("PERINGATAN: %s tidak ada atau kosong; semua kata di luar kamus jadi REVIEW." % WORDLIST.name)

    p = Path(a.artikel)
    if not p.is_file():
        print("GAGAL: berkas '%s' tidak ada. Periksa nama dan folder (huruf besar kecil dan spasi harus sama)." % a.artikel)
        sys.exit(2)
    try:
        raw = p.read_text(encoding="utf8").replace("\r", "")
    except UnicodeDecodeError as e:
        print("GAGAL: '%s' bukan UTF-8 (byte tidak sah di posisi %d). Simpan ulang berkas sebagai UTF-8." % (p.name, e.start))
        sys.exit(2)
    folder = p.parent
    cli = baca_client(folder)
    kosong = [k for k, v in cli.items() if v.startswith("[") and v.endswith("]") and k != "shortcode"]
    if "shortcode" in cli and "shortcode tombol WA" in cli["shortcode"]:
        kosong.append("shortcode")
    if kosong:
        print("GAGAL: CLIENT.md masih berisi isian bawaan template (%s). Isi semua field dulu "
              "(lihat AGENT.md Section 3)." % ", ".join(sorted(kosong)))
        sys.exit(2)
    nama = cli.get("nama", "")
    url_cli = (cli.get("url") or "").rstrip("/")
    shortcode = cli.get("shortcode", "")
    izin = {w.lower() for w in RE_KATA.findall((nama + " " + (cli.get("istilah") or "")).lower())}

    kw = a.kw
    if not kw:
        m = re.search(r"<a href=\"[^\"]*\"><b><i>([^<]+)</i></b></a>", raw)
        kw = m.group(1).strip() if m else ""
    if not kw and a.draft:
        # Draft tanpa anchor permalink adalah temuan audit, bukan alasan berhenti (kontrak: exit 0).
        teks = teks_tampak(raw)
        g_bahasa, _, _ = cek_bahasa(teks, izin)
        temuan = (["anchor permalink paragraf pertama tidak ada, fokus keyword tidak terdeteksi "
                   "(analisis keyword dilewati; jalankan ulang dengan --kw)"]
                  + g_bahasa + cek_angka(raw) + analisis_ritme(raw))
        print("=" * 60)
        print("AUDIT DRAFT : %s (tanpa keyword)" % p.name)
        print("=" * 60)
        for i, x in enumerate(temuan, 1):
            print("TEMUAN %2d: %s" % (i, x))
        print("-" * 60)
        print("Total %d temuan: bahan Tahap 3 (humanize), bukan penghalang." % len(temuan))
        sys.exit(0)
    if not kw:
        print("GAGAL: fokus keyword tidak terdeteksi (pakai --kw)")
        sys.exit(2)
    izin |= {w.lower() for w in RE_KATA.findall(kw.lower())}

    gagal, peringatan, info = [], [], []
    teks = teks_tampak(raw)
    kata_total = len(teks.split())
    L = [l for l in raw.split("\n") if l.strip()]

    # --- Rank Math ---
    if kata_total < 2000:
        gagal.append("jumlah kata %d < 2000" % kata_total)
    elif kata_total < 2500:
        info.append("jumlah kata %d: di bawah 2500, uji Content Length Rank Math hanya skor sebagian (Google tidak menetapkan panjang)" % kata_total)
    p1 = re.search(r"<p>.*?</p>", raw, re.S)
    p1_teks = re.sub(r"<[^>]+>", " ", p1.group(0)) if p1 else ""
    p1_kata = len(p1_teks.split())
    if p1_kata < 200:
        gagal.append("paragraf pertama %d kata < 200" % p1_kata)
    k_vis = len(re.findall(re.escape(kw), teks))
    dens = k_vis * 100.0 / kata_total if kata_total else 0
    if not (31 <= k_vis <= 34):
        gagal.append("keyword %dx (target template 31-34)" % k_vis)
    if dens < 1.0 or dens > 2.5:
        gagal.append("density %.2f%% di luar 1,0-2,5%%" % dens)
    elif dens > 1.5:
        info.append("density %.2f%%: di atas band skor penuh Rank Math 1-1,5%% (masih sah template)" % dens)
    h2 = [l for l in L if l.strip().startswith("<h2>")]
    k_h2 = sum(1 for h in h2 if kw in h)
    if k_h2 < 2:
        gagal.append("keyword hanya di %d heading h2 (minimal 2)" % k_h2)
    for h in h2 + [l for l in L if l.strip().startswith("<h3>")]:
        if "<b>" in h:
            gagal.append("heading dibold: %s" % h.strip()[:60])
    body = "\n".join(l for l in L if not l.strip().startswith(("<h2>", "<h3>", "<img"))
                     and "Alt text:" not in l)                 # alt blok saran bukan body
    k_body = len(re.findall(re.escape(kw), body))
    k_bold = len(re.findall(r"<b>(?:<i>)?" + re.escape(kw) + r"(?:</i>)?</b>", body))
    if k_body != k_bold:
        gagal.append("keyword di body %dx tetapi hanya %dx dibold" % (k_body, k_bold))
    if kw not in p1_teks:
        gagal.append("keyword tidak ada di paragraf pertama")

    # --- Format WordPress ---
    n_more = raw.count("<!--more-->")
    if n_more != 1:
        gagal.append("<!--more--> ada %d (harus 1, tepat setelah paragraf pertama)" % n_more)
    h_semua = [l for l in L if l.strip().startswith("<h2>")]
    for h in h_semua:
        i = L.index(h)
        prev = next((L[j].strip() for j in range(i - 1, -1, -1) if L[j].strip()), "")
        if prev != "<p>&nbsp;</p>":
            gagal.append("h2 tanpa <p>&nbsp;</p> di depan: %s" % re.sub(r"<[^>]+>", "", h)[:50])
    if re.search(r"<p>&nbsp;</p>\s*\n<h3>", raw):
        gagal.append("ada <p>&nbsp;</p> sebelum h3")
    if not ("<ul>" in raw or "<ol>" in raw):
        gagal.append("tidak ada list ul/ol")
    if re.search(r"<h2>\s*Kesimpulan", raw, re.I):
        gagal.append("ada heading Kesimpulan (dilarang)")
    n_img = len(re.findall(r"<img", raw)) + raw.count("GAMBAR DISINI")
    if not (1 <= n_img <= 3):
        gagal.append("blok gambar %d (harus 1-3)" % n_img)
    for m in re.finditer(r"<img[^>]*>", raw):
        alt = re.search(r'alt="([^"]*)"', m.group(0))
        if not alt or kw not in alt.group(1):
            gagal.append("alt img tidak mengandung keyword: %r" % (alt.group(1) if alt else None))
    baris_akhir = L[-1].strip()
    if shortcode and baris_akhir != shortcode:
        gagal.append("baris terakhir bukan shortcode WA: %r" % baris_akhir[:60])
    if shortcode and raw.count(shortcode) != 1:
        gagal.append("shortcode WA muncul %dx (harus 1, di akhir)" % raw.count(shortcode))
    if "Hubungi Kami Dari Kontak Resmi" not in raw:
        gagal.append("heading kontak baku tidak ada")
    if nama and nama not in raw:
        gagal.append("nama klien '%s' tidak muncul di artikel" % nama)
    for masalah in tag_seimbang(raw):
        gagal.append("tag HTML: " + masalah)
    for m in re.finditer(r'<a href="(https?://[^"]+)"([^>]*)>', raw):
        href, atr = m.group(1), m.group(2)
        if url_cli and href.startswith(url_cli):
            continue
        if "wa.me" in href:
            continue                                          # tautan kontak WA: pola template, tanpa target
        if "target=\"_blank\"" not in atr or "noopener" not in atr:
            gagal.append("tautan luar tanpa target/rel: %s" % href[:60])
    if url_cli and url_cli not in raw:
        gagal.append("tautan internal ke %s tidak ada" % url_cli)
    if "wikipedia.org" not in raw:
        gagal.append("tautan Wikipedia kota tidak ada")
    elif "rel=\"noopener noreferrer\"" not in raw.split("wikipedia.org")[1][:200]:
        gagal.append("tautan Wikipedia tanpa rel noopener noreferrer")

    # --- Judul SEO, deskripsi meta, slug (hanya gerbang final) ---
    if not a.draft:
        g_meta, w_meta, i_meta = cek_meta(p, raw, kw)
        gagal += g_meta
        peringatan += w_meta
        info += i_meta
        g_lintas, w_lintas = cek_lintas(p, raw, kw)
        gagal += g_lintas
        peringatan += w_lintas

    # --- Anti-Typo Gate ---
    g_bahasa, w_bahasa, unik = cek_bahasa(teks, izin)
    gagal += g_bahasa
    gagal += cek_angka(raw)
    peringatan += w_bahasa

    # --- Mode draft: audit, bukan gerbang ---
    if a.draft:
        temuan_ritme = analisis_ritme(raw)
        kata_tinjau = [w for w in peringatan if re.fullmatch(r"[a-zà-ÿ-]+", w)]
        lainnya = [w for w in peringatan if not re.fullmatch(r"[a-zà-ÿ-]+", w)]
        semua_temuan = gagal + lainnya + temuan_ritme
        if kata_tinjau:
            semua_temuan.append("%d kata tidak terverifikasi kamus/wordlist (tinjauan manual, "
                                "atau tambahkan ke kamus-kata.txt bila memang baku): %s"
                                % (len(kata_tinjau), " ".join(kata_tinjau[:40])
                                   + (" ..." if len(kata_tinjau) > 40 else "")))
        print("=" * 60)
        print("AUDIT DRAFT : %s" % p.name)
        print("Kata        : %d | keyword %dx (%.2f%%) | h2 berkeyword %d | P1 %d kata"
              % (kata_total, k_vis, dens, k_h2, p1_kata))
        print("=" * 60)
        for i, x in enumerate(semua_temuan, 1):
            print("TEMUAN %2d: %s" % (i, x))
        for x in info:
            print("INFO    : %s" % x)
        print("-" * 60)
        print("Total %d temuan + %d info: bahan Tahap 3 (humanize), bukan penghalang."
              % (len(semua_temuan), len(info)))
        sys.exit(0)

    # --- Laporan ---
    print("=" * 60)
    print("Artikel : %s" % p.name)
    print("Kata    : %d | keyword %dx (%.2f%%) | h2 berkeyword %d" % (kata_total, k_vis, dens, k_h2))
    print("P1      : %d kata" % p1_kata)
    print("=" * 60)
    for jenis, daftar in (("FAIL", gagal), ("WARN", peringatan), ("INFO", info)):
        for x in daftar:
            print("%s: %s" % (jenis, x))
    print("-" * 60)
    print("Hasil: %d FAIL, %d WARN, %d INFO" % (len(gagal), len(peringatan), len(info)))
    sys.exit(1 if gagal else 0)


if __name__ == "__main__":
    main()
