from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def format_rupiah(angka):
    return f"{angka:,.0f}".replace(",", ".")


kurs = pd.read_csv("data/kurs_harian.csv", parse_dates=["tanggal"])
tabel = kurs.pivot(index="tanggal", columns="mata_uang", values="kurs_idr")

ringkasan = pd.DataFrame({
    "awal": tabel.iloc[0],
    "terakhir": tabel.iloc[-1],
    "tertinggi": tabel.max(),
    "terendah": tabel.min(),
    "rata_rata": tabel.mean().round(0),
})
ringkasan["perubahan_persen"] = ((ringkasan["terakhir"] / ringkasan["awal"] - 1) * 100).round(2)

print("Periode:", tabel.index.min().date(), "sampai", tabel.index.max().date())
print(ringkasan)

Path("output").mkdir(exist_ok=True)

fig, sumbu = plt.subplots(2, 2, figsize=(10, 6), sharex=True)
for ax, kode in zip(sumbu.flatten(), tabel.columns):
    ax.plot(tabel.index, tabel[kode], color="#2f6f8f")
    terakhir = format_rupiah(tabel[kode].iloc[-1])
    ax.set_title(f"{kode} terhadap rupiah (terakhir: Rp{terakhir})")
    ax.set_ylabel("Rupiah")
fig.autofmt_xdate()
fig.tight_layout()
fig.savefig("output/tren_kurs.png", dpi=150)

data_harian = tabel.reset_index()
data_harian["tanggal"] = data_harian["tanggal"].dt.date

with pd.ExcelWriter("output/laporan_kurs.xlsx") as penulis:
    ringkasan.to_excel(penulis, sheet_name="Ringkasan")
    data_harian.to_excel(penulis, sheet_name="Data harian", index=False)

print("Tersimpan: output/tren_kurs.png dan output/laporan_kurs.xlsx")