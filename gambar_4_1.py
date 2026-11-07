"""Gambar 4.1: perbandingan data historis, LLGR, dan NLS.

Letakkan file ini satu folder dengan data.py, llgr.py, dan nls(1).py.
Jalankan: python gambar_4_1.py
Hasil: gambar_4_1.png (300 dpi) dan gambar_4_1.svg (vektor).
"""

from pathlib import Path
import runpy
import numpy as np
import matplotlib.pyplot as plt

from data import tahun, P_aktual
from llgr import M as M_llgr, r as r_llgr

# Berkas NLS dari pengguna bernama nls(1).py, sehingga dimuat lewat runpy.
FOLDER = Path(__file__).resolve().parent
nls = runpy.run_path(str(FOLDER / "nls.py"))
M_nls, r_nls = float(nls["M"]), float(nls["r"])

P0 = float(P_aktual[0])
tahun_awal = int(tahun[0])


def model_logistik(t, M, r):
    """Solusi analitis model logistik dengan kapasitas awal tetap."""
    return M / (1 + ((M - P0) / P0) * np.exp(-r * t))


def rmse(hasil_model):
    return np.sqrt(np.mean((P_aktual - hasil_model) ** 2))


def buat_gambar():
    # Buat kurva halus dalam rentang tahun yang benar-benar diamati (2019–2025).
    tahun_kurva = np.linspace(tahun[0], tahun[-1], 601)
    t_kurva = tahun_kurva - tahun_awal

    pred_llgr = model_logistik(tahun - tahun_awal, M_llgr, r_llgr)
    pred_nls = model_logistik(tahun - tahun_awal, M_nls, r_nls)

    fig, ax = plt.subplots(figsize=(10.5, 5.8))
    ax.plot(
        tahun_kurva,
        model_logistik(t_kurva, M_llgr, r_llgr),
        label="LLGR",
        linewidth=2.5,
        color="#2563eb",
    )
    ax.plot(
        tahun_kurva,
        model_logistik(t_kurva, M_nls, r_nls),
        label="NLS",
        linewidth=2.5,
        color="#ea580c",
    )
    ax.scatter(
        tahun,
        P_aktual,
        label="Data historis",
        marker="o",
        s=65,
        color="#111827",
        zorder=5,
    )

    ax.set_title(
        "Perbandingan Data Historis dan Hasil Estimasi Model Logistik",
        fontsize=14,
        fontweight="bold",
        pad=15,
    )
    ax.set_xlabel("Tahun", fontsize=11)
    ax.set_ylabel("Kapasitas IT terbangun (MW)", fontsize=11)
    ax.set_xticks(tahun)
    ax.set_xlim(tahun[0] - 0.2, tahun[-1] + 0.2)
    ax.grid(True, linewidth=0.7, alpha=0.25)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Susun legenda agar urutannya: data historis, LLGR, dan NLS.
    handles, labels = ax.get_legend_handles_labels()
    urutan = [labels.index(nama) for nama in ("Data historis", "LLGR", "NLS")]
    ax.legend(
        [handles[i] for i in urutan],
        [labels[i] for i in urutan],
        loc="upper left",
        frameon=True,
        fontsize=10,
    )

    fig.tight_layout()
    fig.savefig(FOLDER / "gambar_4_1.png", dpi=300, bbox_inches="tight")
    fig.savefig(FOLDER / "gambar_4_1.svg", bbox_inches="tight")
    plt.close(fig)

    print("Gambar 4.1 berhasil disimpan.")
    print(
        f"LLGR: M = {M_llgr:.6f} MW; r = {r_llgr:.8f}; RMSE = {rmse(pred_llgr):.4f} MW"
    )
    print(f"NLS : M = {M_nls:.6f} MW; r = {r_nls:.8f}; RMSE = {rmse(pred_nls):.4f} MW")


if __name__ == "__main__":
    buat_gambar()
