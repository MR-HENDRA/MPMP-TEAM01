"""Gambar 4.4: perbandingan tiga skenario perubahan carrying capacity.

Sumber parameter: data.py dan nls(1).py / nls.py dari penelitian.
Metode simulasi: Euler Forward, dt=0,01 tahun, periode 2019-2043.

Cara menjalankan (semua file dalam satu folder):
    pip install numpy scipy matplotlib
    python gambar_4_4.py

Output:
    gambar_4_4.png (300 dpi)
    gambar_4_4.svg (vektor)
    hasil_skenario_M.csv (hasil tiap 0,01 tahun)
"""
from pathlib import Path
import csv
import runpy
import sys

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

FOLDER = Path(__file__).resolve().parent
sys.path.insert(0, str(FOLDER))
from data import P_aktual, tahun

# Gunakan parameter yang dihitung oleh program NLS asli, bukan taksiran baru.
nls_file = FOLDER / "nls(1).py"
if not nls_file.exists():
    nls_file = FOLDER / "nls.py"
if not nls_file.exists():
    raise FileNotFoundError("File nls(1).py atau nls.py harus ada dalam folder yang sama.")

nls = runpy.run_path(str(nls_file))
r = float(nls["r"])
M_baseline = float(nls["M"])
P0 = float(P_aktual[0])
tahun_awal = int(tahun[0])

# Sesuai pengaturan model Insight Maker dalam BAB III.
DT = 0.01               # tahun
DURASI = 24.0           # tahun, 2019 sampai 2043
JUMLAH_LANGKAH = round(DURASI / DT)
t = np.arange(JUMLAH_LANGKAH + 1, dtype=float) * DT
tahun_simulasi = tahun_awal + t


def euler_forward(P_awal: float, r: float, M: float) -> np.ndarray:
    """Integrasikan persamaan dP/dt = r*P*(1-P/M) dengan Euler Forward."""
    hasil = np.empty(JUMLAH_LANGKAH + 1, dtype=float)
    hasil[0] = P_awal
    for i in range(JUMLAH_LANGKAH):
        hasil[i + 1] = hasil[i] + DT * r * hasil[i] * (1 - hasil[i] / M)
    return hasil


# Ubah hanya M, sementara r dan kapasitas awal dibuat sama.
skenario = {
    "Penurunan M 10%": {
        "M": 0.9 * M_baseline,
        "warna": "#D97735",
    },
    "Baseline": {
        "M": M_baseline,
        "warna": "#2161A3",
    },
    "Peningkatan M 10%": {
        "M": 1.1 * M_baseline,
        "warna": "#258C76",
    },
}
for data_skenario in skenario.values():
    data_skenario["P"] = euler_forward(P0, r, data_skenario["M"])


# Angka dengan format Indonesia: 1.689,53, bukan 1,689.53.
def angka_id(n: float, desimal: int = 2) -> str:
    return f"{n:,.{desimal}f}".replace(",", "_").replace(".", ",").replace("_", ".")


plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.titlesize": 15,
    "axes.labelsize": 12,
    "savefig.dpi": 300,
})
fig, ax = plt.subplots(figsize=(11.5, 6.6))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

# Gambar batas M sebagai garis bantu tipis dan kurva kapasitas sebagai garis utama.
for nama, data_skenario in skenario.items():
    M = data_skenario["M"]
    warna = data_skenario["warna"]
    ax.axhline(M, color=warna, linestyle=(0, (5, 5)), linewidth=1, alpha=0.42, zorder=1)
    ax.plot(tahun_simulasi, data_skenario["P"], linewidth=2.7,
            color=warna, label=nama, zorder=3)
    P_akhir = data_skenario["P"][-1]
    ax.scatter([tahun_awal + DURASI], [P_akhir], s=50, color=warna,
               edgecolor="white", linewidth=1.0, zorder=5)
    ax.annotate(f"{angka_id(P_akhir)} MW", xy=(tahun_awal + DURASI, P_akhir),
                xytext=(10, 0), textcoords="offset points", ha="left", va="center",
                fontsize=10.2, fontweight="semibold", color=warna)

ax.set_title("Pengaruh Perubahan Carrying Capacity terhadap Pertumbuhan Kapasitas IT",
             fontweight="semibold", pad=17)
ax.set_xlabel("Tahun", labelpad=8)
ax.set_ylabel("Kapasitas IT (MW)", labelpad=9)
ax.set_xticks(np.arange(2019, 2044, 3))
ax.set_xlim(2018.8, 2047.0)  # ruang kanan untuk label kapasitas akhir
ax.set_ylim(640, 1950)
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: angka_id(x, 0)))
ax.grid(True, color="#B4BFCA", alpha=0.28, linestyle="--", linewidth=0.7)
ax.set_axisbelow(True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.legend(loc="upper left", frameon=True, fontsize=10, framealpha=0.98)
ax.text(0.02, 0.03, "Garis putus-putus menunjukkan batas M masing-masing skenario.",
        transform=ax.transAxes, fontsize=9, color="#5B6470", va="bottom")
fig.tight_layout()
fig.savefig(FOLDER / "gambar_4_4.png", dpi=300, bbox_inches="tight", facecolor="white")
fig.savefig(FOLDER / "gambar_4_4.svg", bbox_inches="tight", facecolor="white")
plt.close(fig)

# Simpan seluruh kurva sebagai data yang dapat diperiksa dengan Excel.
with (FOLDER / "hasil_skenario_M.csv").open("w", encoding="utf-8-sig", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["waktu_t", "tahun", "penurunan_M_10_MW", "baseline_MW", "peningkatan_M_10_MW"])
    for i, waktu in enumerate(t):
        writer.writerow([
            f"{waktu:.2f}", f"{tahun_simulasi[i]:.2f}",
            f"{skenario['Penurunan M 10%']['P'][i]:.6f}",
            f"{skenario['Baseline']['P'][i]:.6f}",
            f"{skenario['Peningkatan M 10%']['P'][i]:.6f}",
        ])

print("Gambar 4.4: perbandingan skenario perubahan M")
print(f"Parameter NLS: r = {r:.8f} per tahun; M baseline = {M_baseline:.6f} MW")
print(f"Metode: Euler Forward; P0 = {P0:.0f} MW; dt = {DT}; durasi = {DURASI:.0f} tahun")
for nama, hasil in skenario.items():
    print(f"{nama}: M = {angka_id(hasil['M'])} MW; P(24) = {angka_id(hasil['P'][-1])} MW")
print("Berkas: gambar_4_4.png, gambar_4_4.svg, hasil_skenario_M.csv")
