"""Gambar 4.6: implikasi hasil simulasi terhadap perencanaan kapasitas sistem TI.

Diagram konseptual yang merangkum temuan tiga skenario pada BAB IV.
Tidak menghitung ulang data; angka spesifik ditampilkan dalam tabel/grafik sebelumnya.

Jalankan:
    pip install matplotlib
    python gambar_4_6_revisi.py

Keluaran dalam folder yang sama:
    gambar_4_6_revisi.png (300 DPI)
    gambar_4_6_revisi.svg (vektor, teks dapat diedit)
"""

from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUTPUT_DIR = Path(__file__).resolve().parent

# Warna dan tipografi diseragamkan untuk laporan akademik.
NAVY = '#203247'
TEXT = '#26374A'
MUTED = '#536575'
CONNECTOR = '#728195'
COLORS = ['#2D67A2', '#26847B', '#B97733']
PALE = ['#F1F6FC', '#EFF9F6', '#FFF6EB']

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 11,
    'savefig.dpi': 300,
    'svg.fonttype': 'none',  # Teks tetap berupa teks pada berkas SVG.
})

fig, ax = plt.subplots(figsize=(16, 9))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.axis('off')

ax.text(
    8, 8.53,
    'Implikasi Hasil Simulasi terhadap Perencanaan Kapasitas Sistem TI',
    ha='center', va='center', fontsize=18.0, fontweight='bold', color=NAVY,
)
ax.text(
    8, 8.15,
    'Pemodelan pertumbuhan logistik kapasitas IT data center di Irlandia',
    ha='center', va='center', fontsize=10.5, color=MUTED,
)
ax.text(0.70, 7.66, 'HASIL SIMULASI', ha='left', va='center',
        fontsize=10, fontweight='bold', color=MUTED)

# Koordinat diatur agar ruang untuk jalur panah terpisah dari isi setiap kotak.
COLUMNS = [0.65, 5.72, 10.79]
CARD_W = 4.55
TOP_Y = 5.05
BOTTOM_Y = 0.76
CARD_H = 2.37
CENTERS = [x + CARD_W / 2 for x in COLUMNS]


def add_card(x, y, color, bg, title, lines, number):
    """Satu kartu dengan judul dan maksimal empat baris teks."""
    panel = FancyBboxPatch(
        (x, y), CARD_W, CARD_H,
        boxstyle='round,pad=0.01,rounding_size=0.18',
        facecolor=bg, edgecolor=color, linewidth=1.35, zorder=3,
    )
    ax.add_patch(panel)
    # Bilah aksen tetap berada dalam kotak, bukan pada teks.
    ax.plot([x + 0.23, x + CARD_W - 0.23], [y + CARD_H - 0.76]*2,
            color=color, alpha=0.34, linewidth=1.1, zorder=4)
    num = FancyBboxPatch(
        (x + 0.25, y + CARD_H - 0.56), 0.42, 0.34,
        boxstyle='round,pad=0.03,rounding_size=0.08',
        facecolor=color, edgecolor='none', zorder=5,
    )
    ax.add_patch(num)
    ax.text(x + 0.46, y + CARD_H - 0.39, str(number),
            color='white', fontsize=9.4, fontweight='bold',
            ha='center', va='center', zorder=6)
    ax.text(x + 0.81, y + CARD_H - 0.39, title,
            color=NAVY, fontsize=12.6, fontweight='bold',
            ha='left', va='center', zorder=6)
    # Teks isi sengaja ditaruh jauh dari garis konektor pada luar kotak.
    body_top = y + CARD_H - 1.10
    for i, line in enumerate(lines):
        ax.text(x + 0.31, body_top - 0.34*i, line,
                ha='left', va='center', fontsize=11.2,
                color=TEXT, zorder=6)


TOP = [
    ('Skenario Baseline', [
        'Kapasitas tumbuh secara logistik',
        'dan mendekati batas keseimbangan',
        'secara bertahap.',
    ]),
    ('Perubahan Nilai M', [
        'Nilai M yang lebih tinggi mendorong',
        'kapasitas akhir lebih besar;',
        'M yang lebih rendah membatasinya.',
    ]),
    ('Skenario Intervensi', [
        'Penurunan r pada 2026–2028',
        'memperlambat pertumbuhan tanpa',
        'mengubah batas keseimbangan M.',
    ]),
]
BOTTOM = [
    ('Perencanaan Infrastruktur', [
        'Antisipasi kebutuhan listrik,',
        'jaringan, lahan, dan fasilitas',
        'pendukung pengembangan kapasitas.',
    ]),
    ('Manajemen Kapasitas', [
        'Terapkan ekspansi bertahap dan',
        'pantau penggunaan sumber daya',
        'sesuai kebutuhan layanan.',
    ]),
    ('Mitigasi Risiko', [
        'Siapkan cadangan kapasitas dan',
        'rencana pemulihan operasional',
        'untuk menghadapi gangguan.',
    ]),
]

for i, x in enumerate(COLUMNS):
    add_card(x, TOP_Y, COLORS[i], PALE[i], TOP[i][0], TOP[i][1], i + 1)
    add_card(x, BOTTOM_Y, COLORS[i], PALE[i], BOTTOM[i][0], BOTTOM[i][1], i + 1)

# Hubungan atas: seluruh garis berada DI BAWAH kotak atas dan DI ATAS kotak pusat.
# Tidak ada garis yang melewati area tulisan.
UPPER_BUS = 4.77
ax.plot([CENTERS[0], CENTERS[2]], [UPPER_BUS, UPPER_BUS],
        color=CONNECTOR, linewidth=1.8, zorder=1)
for xc in CENTERS:
    ax.plot([xc, xc], [TOP_Y, UPPER_BUS],
            color=CONNECTOR, linewidth=1.8, zorder=1)

HUB_X, HUB_Y, HUB_W, HUB_H = 5.32, 3.77, 5.36, 0.71
HUB_CENTER = HUB_X + HUB_W / 2
ax.add_patch(FancyArrowPatch(
    (HUB_CENTER, UPPER_BUS), (HUB_CENTER, HUB_Y + HUB_H),
    arrowstyle='-|>', mutation_scale=15, linewidth=1.8,
    color=CONNECTOR, zorder=2,
))

hub = FancyBboxPatch(
    (HUB_X, HUB_Y), HUB_W, HUB_H,
    boxstyle='round,pad=0.01,rounding_size=0.20',
    facecolor=NAVY, edgecolor=NAVY, linewidth=1.0, zorder=3,
)
ax.add_patch(hub)
ax.text(HUB_CENTER, HUB_Y + HUB_H/2,
        'IMPLIKASI PERENCANAAN KAPASITAS TI',
        color='white', fontsize=13.4, fontweight='bold',
        ha='center', va='center', zorder=4)

# Hubungan bawah: panah berakhir tepat di tepi atas kotak rekomendasi.
LOWER_BUS = 3.43
ax.plot([HUB_CENTER, HUB_CENTER], [HUB_Y, LOWER_BUS],
        color=CONNECTOR, linewidth=1.8, zorder=1)
ax.plot([CENTERS[0], CENTERS[2]], [LOWER_BUS, LOWER_BUS],
        color=CONNECTOR, linewidth=1.8, zorder=1)
for xc in CENTERS:
    ax.add_patch(FancyArrowPatch(
        (xc, LOWER_BUS), (xc, BOTTOM_Y + CARD_H + 0.025),
        arrowstyle='-|>', mutation_scale=15, linewidth=1.8,
        color=CONNECTOR, zorder=2,
    ))

ax.text(8, 0.29,
        'Catatan: M merupakan estimasi statistik, bukan batas fisik maksimum yang terverifikasi.',
        ha='center', va='center', fontsize=9.4, color=MUTED)

fig.subplots_adjust(left=0.015, right=0.985, top=0.985, bottom=0.02)
for ext in ('png', 'svg'):
    target = OUTPUT_DIR / f'gambar_4_6_revisi.{ext}'
    fig.savefig(target, dpi=300, facecolor='white')
    print(f'Tersimpan: {target}')
plt.close(fig)
