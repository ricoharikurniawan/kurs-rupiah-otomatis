import pandas as pd
import requests

MATA_UANG = ["USD", "EUR", "SGD", "CNY"]
MULAI = "2026-08-01"
SELESAI = "2026-09-30"

baris = []
for kode in MATA_UANG:
    url = f"https://api.frankfurter.dev/v1/{MULAI}..{SELESAI}"
    respons = requests.get(url, params={"base": kode, "symbols": "IDR"}, timeout=30)
    respons.raise_for_status()
    rates = respons.json()["rates"]
    for tanggal, kurs in rates.items():
        baris.append({"tanggal": tanggal, "mata_uang": kode, "kurs_idr": kurs["IDR"]})

kurs = pd.DataFrame(baris)
kurs["tanggal"] = pd.to_datetime(kurs["tanggal"])

print(len(kurs))
print(kurs.head())
print(kurs.groupby("mata_uang").size())
print(kurs["tanggal"].min(), kurs["tanggal"].max())