import pandas as pd
import requests

MATA_UANG = ["USD", "EUR", "SGD", "CNY"]


def ambil_kurs(mulai, selesai):
    baris = []
    for kode in MATA_UANG:
        url = f"https://api.frankfurter.dev/v1/{mulai}..{selesai}"
        respons = requests.get(url, params={"base": kode, "symbols": "IDR"}, timeout=30)
        respons.raise_for_status()
        for tanggal, kurs in respons.json()["rates"].items():
            baris.append({"tanggal": tanggal, "mata_uang": kode, "kurs_idr": kurs["IDR"]})
    tabel = pd.DataFrame(baris, columns=["tanggal", "mata_uang", "kurs_idr"])
    tabel["tanggal"] = pd.to_datetime(tabel["tanggal"])
    return tabel