"""Gambar 4.3: titik infleksi model logistik NLS.

Letakkan file ini satu folder bersama data.py dan nls(1).py.
Jalankan: python gambar_4_3.py
Hasil: gambar_4_3.png dan gambar_4_3.svg
"""

from pathlib import Path
import importlib.util
import sys

import numpy as np
import matplotlib.pyplot as plt

FOLDER = Path(__file__).resolve().parent
sys.path.insert(0, str(FOLDER))
from data import tahun, P_aktual

# Baca hasil estimasi dari program NLS yang sudah dipakai pada BAB IV.
NLS_FILE = FOLDER / "nls(1).py"
if not NLS_FILE.exists():
    NLS_FILE = FOLDER / "nls.py"
if not NLS_FILE.exists():
    raise FileNotFoundError("Letakkan nls(1).py atau nls.py pada folder yang sama.")
spec = importlib.util.spec_from_file_location("model_nls_untuk_gambar43", NLS_FILE)
modul_nls = importlib.util.module_from_spec(spec)
spec.loader.exec_module(modul_nls)

M = float(modul_nls.M)
r = float(modul_nls.r)
P0 = float(P_aktual[0])
tahun_awal = int(tahun[0])

# Titik infleksi logistik kontinu: P = M/2.
P_inf = M / 2
t_inf = np.log((M - P0) / P0) / r
tahun_inf = tahun_awal + t_inf

# Tampilkan bagian awal simulasi agar posisi titik infleksi mudah dilihat.
t = np.linspace(0, 6, 601)
P_model = M / (1 + ((M - P0) / P0) * np.exp(-r * t))

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.titlesize": 15,
        "axes.labelsize": 11,
        "savefig.dpi": 300,
    }
)
fig, ax = plt.subplots(figsize=(10.8, 6.2))
ax.plot(
    tahun_awal + t,
    P_model,
    color="#1f5aa6",
    linewidth=2.6,
    label="Model logistik (NLS)",
    zorder=2,
)
ax.scatter(
    tahun, P_aktual, s=40, color="#28333c", alpha=0.83, label="Data historis", zorder=4
)
ax.axhline(
    P_inf,
    linestyle="--",
    linewidth=1.5,
    color="#b36a1f",
    label=f"Setengah M = {P_inf:,.2f} MW",
    zorder=1,
)
ax.vlines(
    tahun_inf, 660, P_inf, colors="#b36a1f", linewidth=1.5, linestyles=":", zorder=2
)
ax.scatter(
    [tahun_inf],
    [P_inf],
    color="#bb3c32",
    s=100,
    edgecolors="white",
    linewidth=1.2,
    zorder=6,
    label="Titik infleksi",
)
ax.annotate(
    f"Titik infleksi\nt = {t_inf:.2f} tahun\nP = {P_inf:.2f} MW",
    xy=(tahun_inf, P_inf),
    xytext=(tahun_inf + 1.15, P_inf + 125),
    arrowprops={"arrowstyle": "->", "color": "#bb3c32", "lw": 1.4},
    fontsize=10,
    color="#8c2923",
    ha="left",
    va="center",
    bbox={"boxstyle": "round,pad=0.35", "fc": "white", "ec": "#dddddd", "alpha": 0.95},
)
ax.set_title(
    "Titik Infleksi Pertumbuhan Kapasitas IT Data Center", pad=15, fontweight="bold"
)
ax.set_xlabel("Tahun")
ax.set_ylabel("Kapasitas IT (MW)")
ax.set_xticks(np.arange(2019, 2026))
ax.set_xlim(2018.85, 2025.18)
ax.set_ylim(660, 1460)
ax.grid(True, linestyle="--", linewidth=0.6, alpha=0.32)
ax.legend(loc="lower right", framealpha=0.97, fontsize=9)
fig.tight_layout()
fig.savefig(FOLDER / "gambar_4_3.png", bbox_inches="tight")
fig.savefig(FOLDER / "gambar_4_3.svg", bbox_inches="tight")
plt.close(fig)

print(f"Estimasi NLS: r = {r:.8f}/tahun; M = {M:.6f} MW")
print(f"Titik infleksi: t = {t_inf:.5f}, tahun = {tahun_inf:.5f}, P = {P_inf:.5f} MW")
print("Tersimpan: gambar_4_3.png dan gambar_4_3.svg")
