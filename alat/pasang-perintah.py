#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pasang perintah /artikel ke agent yang dipakai di komputer ini.

Sumber tunggal: perintah/artikel.md (netral, tanpa format khusus agent). Skrip ini membuat salinan
dengan format yang dipahami tiap agent. Hasilnya TIDAK ikut repo (folder agent ada di .gitignore),
jadi setiap karyawan menjalankan skrip ini sekali di komputernya.

Pakai (dari root project):
  python -I -X utf8 alat/pasang-perintah.py --daftar            lihat agent yang didukung
  python -I -X utf8 alat/pasang-perintah.py trae                pasang untuk TRAE (di project ini)
  python -I -X utf8 alat/pasang-perintah.py claude zcode        pasang beberapa sekaligus
  python -I -X utf8 alat/pasang-perintah.py semua               pasang ke semua agent yang didukung
  python -I -X utf8 alat/pasang-perintah.py trae --global       pasang untuk semua project (folder rumah)
  python -I -X utf8 alat/pasang-perintah.py trae --cek          hanya periksa, tanpa menulis

Agent tanpa folder command (Codex, Cursor, dan lainnya) tidak dipasang. Untuk mereka, tulis di chat:
  Baca AGENT.md, lalu kerjakan <nama perusahaan> bulan <bulan> sesuai Section 10.

Author: Mas Wondho - Duta Corpora Indonesia (DCI)
Copyright (c) 2026 Duta Corpora Indonesia - All rights reserved
"""
import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUMBER = ROOT / "perintah" / "artikel.md"
NAMA = "artikel"
DESKRIPSI = ("DCI SEO Auditor: kerjakan artikel SEO satu klien untuk satu bulan "
             "(audit, humanize, cek ZeroGPT, laporan). Argumen: <nama perusahaan> <bulan> [tahun]")

# Tiap agent: folder command project (relatif ke root repo), folder command global (relatif ke
# folder rumah), format kepala berkas, dan cara menyisipkan argumen.
#   kepala  : "trae" memakai kunci Name/Description (huruf besar), "markdown" memakai description/argument-hint.
#   argumen : teks pengganti {{ARGUMEN}}.
AGEN = {
    "trae": {
        "project": ".trae/commands", "global": ".trae/commands", "kepala": "trae",
        "argumen": "yang operator tulis setelah /artikel",
        "sumber": "https://docs.trae.ai/ide/slash-commands",
    },
    "zcode": {
        "project": ".zcode/commands", "global": ".zcode/commands", "kepala": "markdown",
        "argumen": "yang operator tulis setelah /artikel",
        "sumber": "https://zcode.z.ai/en/newdocs/commands",
    },
    "claude": {
        "project": ".claude/commands", "global": ".claude/commands", "kepala": "markdown",
        "argumen": "$ARGUMENTS",
        "sumber": "https://code.claude.com/docs/en/slash-commands",
    },
}


def python_cmd():
    return "python" if os.name == "nt" else "python3"


def kepala(jenis):
    if jenis == "trae":
        return "---\nName: %s\nDescription: %s\n---\n\n" % (NAMA, DESKRIPSI)
    return "---\ndescription: %s\nargument-hint: <nama perusahaan> <bulan> [tahun]\n---\n\n" % DESKRIPSI


def bangun(info):
    isi = SUMBER.read_text(encoding="utf8")
    isi = isi.replace("{{ARGUMEN}}", info["argumen"]).replace("{{PYTHON}}", python_cmd())
    return kepala(info["kepala"]) + isi


def tujuan(info, global_):
    if global_:
        return Path.home() / info["global"] / (NAMA + ".md")
    return ROOT / info["project"] / (NAMA + ".md")


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("agen", nargs="*", help="trae, zcode, claude, atau semua")
    ap.add_argument("--daftar", action="store_true")
    ap.add_argument("--global", dest="global_", action="store_true",
                    help="pasang ke folder rumah (berlaku di semua project), bukan hanya project ini")
    ap.add_argument("--cek", action="store_true", help="periksa saja, jangan menulis berkas")
    a = ap.parse_args()

    if not SUMBER.is_file():
        print("GAGAL: sumber perintah '%s' tidak ada. Jalankan dari repo DCI SEO Auditor." % SUMBER)
        sys.exit(2)
    if a.daftar or not a.agen:
        print("Agent yang didukung:")
        for k, v in AGEN.items():
            print("  %-7s project: %-20s global: ~/%s   (%s)" % (k, v["project"], v["global"], v["sumber"]))
        print("\nAgent lain (Codex, Cursor, dan sebagainya): tulis di chat "
              "'Baca AGENT.md, lalu kerjakan <perusahaan> bulan <bulan> sesuai Section 10.'")
        sys.exit(0 if a.daftar else 2)

    pilih = list(AGEN) if "semua" in a.agen else a.agen
    salah = [x for x in pilih if x not in AGEN]
    if salah:
        print("GAGAL: agent tidak dikenal: %s. Pilihan: %s, semua." % (", ".join(salah), ", ".join(AGEN)))
        sys.exit(2)

    for k in pilih:
        info = AGEN[k]
        t = tujuan(info, a.global_)
        isi = bangun(info)
        if "{{" in isi:
            print("GAGAL: placeholder belum terganti di perintah untuk %s." % k)
            sys.exit(1)
        if a.cek:
            ada = t.is_file()
            sama = ada and t.read_text(encoding="utf8") == isi
            print("%-7s %s -> %s" % (k, "sudah terpasang dan terbaru" if sama else
                                    ("terpasang tetapi berbeda (jalankan ulang untuk memperbarui)" if ada else "belum terpasang"), t))
            continue
        t.parent.mkdir(parents=True, exist_ok=True)
        t.write_text(isi, encoding="utf8", newline="\n")
        print("%-7s terpasang: %s" % (k, t))
    if not a.cek:
        print("\nMuat ulang agent atau buka sesi baru, lalu ketik /artikel <perusahaan> <bulan>.")


if __name__ == "__main__":
    main()
