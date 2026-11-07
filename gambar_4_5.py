"""Gambar 4.5: skenario baseline dan intervensi laju pertumbuhan.

Gunakan bersama data.py dan nls(1).py (atau nls.py) dalam satu folder.

Jalankan:
    pip install numpy scipy matplotlib
    python gambar_4_5.py

Output:
    gambar_4_5.png          Grafik untuk BAB IV (300 DPI)
    gambar_4_5.svg          Grafik vektor
    hasil_skenario_intervensi.csv  Data simulasi setiap 0,01 tahun

Metode: Euler Forward. Periode 2019-2043, dt=0,01 tahun.
Intervensi: r turun 20% dari t=7 sampai sebelum t=10 (2026-2028),
            lalu kembali normal mulai t=10 (2029).
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

nls_file = FOLDER / "nls(1).py"
if not nls_file.exists():
    nls_file = FOLDER / "nls.py"
if not nls_file.exists():
    raise FileNotFoundError("Letakkan nls(1).py atau nls.py satu folder dengan program ini.")

nls = runpy.run_path(str(nls_file))
r_normal = float(nls["r"])
M = float(nls["M"])
P0 = float(P_aktual[0])
tahun_awal = int(tahun[0])

DT = 0.01
DURASI = 24.0
TAHUN_MULAI_INTERVENSI = 7.0  # 2026
TAHUN_AKHIR_INTERVENSI = 10.0  # 2029, tidak termasuk
FAKTOR_INTERVENSI = 0.8  # Penurunan 20%

jumlah_langkah = round(DURASI / DT)
t = np.arange(jumlah_langkah + 1, dtype=float) * DT
tahun_kalender = tahun_awal + t


def euler_forward(intervensi: bool):
    """Hitung perkembangan P(t) serta r(t) untuk baseline/intervensi."""
    P = np.empty(jumlah_langkah + 1, dtype=float)
    r_series = np.empty(jumlah_langkah + 1, dtype=float)
    P[0] = P0
    for i in range(jumlah_langkah):
        r_saat_ini = (
            r_normal * FAKTOR_INTERVENSI
            if intervensi and TAHUN_MULAI_INTERVENSI <= t[i] < TAHUN_AKHIR_INTERVENSI
            else r_normal
        )
        r_series[i] = r_saat_ini
        P[i+1] = P[i] + DT * r_saat_ini * P[i] * (1 - P[i] / M)
    r_series[-1] = r_normal
    return P, r_series


P_baseline, r_baseline = euler_forward(False)
P_intervensi, r_intervensi = euler_forward(True)


def angka_id(nilai: float, desimal: int = 2):
    return f"{nilai:,.{desimal}f}".replace(",", "_").replace(".", ",").replace("_", ".")


def pada_tahun(tahun_target: int):
    idx = round((tahun_target - tahun_awal) / DT)
    return P_baseline[idx], P_intervensi[idx]

# Visualisasi konsisten dengan gaya Gambar 4.4 dan judul tebal.
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.titlesize": 15,
    "axes.labelsize": 12,
    "savefig.dpi": 300,
})

warna_baseline = "#2161A3"
warna_intervensi = "#D97735"
warna_pita = "#F2C892"
fig, ax = plt.subplots(figsize=(11.5, 6.7))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

ax.axvspan(2026, 2029, color=warna_pita, alpha=0.29,
           label="Periode intervensi (2026–2028)", zorder=0)
ax.plot(tahun_kalender, P_baseline, color=warna_baseline, linewidth=2.7,
        label="Baseline", zorder=3)
ax.plot(tahun_kalender, P_intervensi, color=warna_intervensi, linewidth=2.7,
        linestyle="--", label="Intervensi (r turun 20%)", zorder=4)

# Penanda awal dan akhir periode pengurangan r.
for tahun_acuan in (2026, 2029):
    ax.axvline(tahun_acuan, color="#A86B36", alpha=0.52, linewidth=1.1,
               linestyle=(0, (3, 4)), zorder=1)

P_b_2029, P_i_2029 = pada_tahun(2029)
ax.scatter([2029], [P_b_2029], color=warna_baseline, s=48,
           edgecolor="white", linewidth=0.8, zorder=6)
ax.scatter([2029], [P_i_2029], color=warna_intervensi, s=48,
           edgecolor="white", linewidth=0.8, zorder=6)

ax.set_title("Perbandingan Pertumbuhan Kapasitas IT: Baseline dan Intervensi",
             fontweight="bold", pad=18)
ax.set_xlabel("Tahun", labelpad=8)
ax.set_ylabel("Kapasitas IT (MW)", labelpad=9)
ax.set_xlim(2018.65, 2043.6)
ax.set_ylim(630, 1760)
ax.set_xticks([2019, 2022, 2025, 2026, 2029, 2032, 2035, 2038, 2041, 2043])
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: angka_id(x, 0)))
ax.grid(True, color="#AAB6C3", alpha=0.30, linestyle="--", linewidth=0.7)
ax.set_axisbelow(True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.legend(loc="upper left", framealpha=0.97, fontsize=9.5)

# Pembesaran agar perbedaan kurva di sekitar akhir intervensi mudah dilihat.
ax_zoom = ax.inset_axes([0.49, 0.16, 0.46, 0.38])
ax_zoom.set_facecolor("white")
ax_zoom.axvspan(2026, 2029, color=warna_pita, alpha=0.30, zorder=0)
ax_zoom.plot(tahun_kalender, P_baseline, color=warna_baseline,
             linewidth=2.15, zorder=3)
ax_zoom.plot(tahun_kalender, P_intervensi, color=warna_intervensi,
             linewidth=2.15, linestyle="--", zorder=4)
ax_zoom.scatter([2029], [P_b_2029], color=warna_baseline,
                s=30, edgecolor="white", linewidth=0.6, zorder=6)
ax_zoom.scatter([2029], [P_i_2029], color=warna_intervensi,
                s=30, edgecolor="white", linewidth=0.6, zorder=6)
ax_zoom.vlines(2029, P_i_2029, P_b_2029, color="#5D6471", lw=1.2,
               linestyle=":", zorder=5)
ax_zoom.set_xlim(2025.5, 2031.1)
ax_zoom.set_ylim(1415, 1655)
ax_zoom.set_xticks([2026, 2027, 2028, 2029, 2030, 2031])
ax_zoom.tick_params(labelsize=8)
ax_zoom.grid(True, alpha=0.22, linewidth=0.5)
ax_zoom.set_title("Pembesaran periode intervensi", fontweight="semibold",
                  fontsize=9.5, pad=6)
ax_zoom.text(0.04, 0.94,
             f"Selisih pada 2029: {angka_id(P_b_2029 - P_i_2029)} MW",
             transform=ax_zoom.transAxes, fontsize=8.9, fontweight="semibold",
             ha="left", va="top", color="#373D46",
             bbox={"boxstyle": "round,pad=0.3", "fc": "white", "ec": "#DADFE5", "alpha": 0.95})
for spine in ax_zoom.spines.values():
    spine.set_color("#9BA8B5")
    spine.set_linewidth(1.0)

ax.text(0.025, 0.035,
        "Pita warna menandai penurunan r selama 2026–2028; kedua skenario memiliki M yang sama.",
        transform=ax.transAxes, fontsize=9.0, color="#505C66", va="bottom")

fig.tight_layout()
fig.savefig(FOLDER / "gambar_4_5.png", dpi=300, bbox_inches="tight", facecolor="white")
fig.savefig(FOLDER / "gambar_4_5.svg", bbox_inches="tight", facecolor="white")
plt.close(fig)

with (FOLDER / "hasil_skenario_intervensi.csv").open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["waktu_t", "tahun", "r_baseline", "r_intervensi",
                     "kapasitas_baseline_MW", "kapasitas_intervensi_MW", "selisih_MW"])
    for i in range(jumlah_langkah + 1):
        writer.writerow([f"{t[i]:.2f}", f"{tahun_kalender[i]:.2f}",
                         f"{r_baseline[i]:.10f}", f"{r_intervensi[i]:.10f}",
                         f"{P_baseline[i]:.6f}", f"{P_intervensi[i]:.6f}",
                         f"{P_baseline[i] - P_intervensi[i]:.6f}"])

print("Gambar 4.5: baseline dan intervensi (Euler Forward)")
print(f"Parameter NLS: r = {r_normal:.10f} per tahun; M = {M:.6f} MW")
print(f"Nilai r saat intervensi = {r_normal * FAKTOR_INTERVENSI:.10f} per tahun")
for tahun_target in (2026, 2029, 2043):
    p_b, p_i = pada_tahun(tahun_target)
    print(f"{tahun_target}: baseline {angka_id(p_b)} MW; "
          f"intervensi {angka_id(p_i)} MW; selisih {angka_id(p_b-p_i)} MW")
print("Berkas: gambar_4_5.png, gambar_4_5.svg, hasil_skenario_intervensi.csv")
