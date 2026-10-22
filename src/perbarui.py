from datetime import date
from pathlib import Path

import pandas as pd

from sumber import ambil_kurs

FILE = Path("data/kurs_harian.csv")
MULAI_AWAL = "2026-08-01"

hari_ini = date.today().isoformat()

if FILE.exists():
    lama = pd.read_csv(FILE, parse_dates=["tanggal"])
    mulai = lama["tanggal"].max().date().isoformat()
else:
    lama = None
    mulai = MULAI_AWAL

print("mengambil data dari", mulai, "sampai", hari_ini)
baru = ambil_kurs(mulai, hari_ini)

if lama is None:
    gabung = baru
    jumlah_lama = 0
else:
    gabung = pd.concat([lama, baru], ignore_index=True)
    jumlah_lama = len(lama)

gabung = gabung.drop_duplicates(subset=["tanggal", "mata_uang"], keep="last")
gabung = gabung.sort_values(["mata_uang", "tanggal"]).reset_index(drop=True)

FILE.parent.mkdir(exist_ok=True)
gabung.to_csv(FILE, index=False)

print("baris sebelumnya:", jumlah_lama)
print("baris sekarang:", len(gabung))
print("tambahan baru:", len(gabung) - jumlah_lama)
print("data terakhir:", gabung["tanggal"].max().date())